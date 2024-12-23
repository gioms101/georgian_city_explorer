from datetime import datetime, time, timedelta
from django.utils.timezone import now
from rest_framework import serializers
from .models import Event
from main.models import Location


class EventSerializer(serializers.ModelSerializer):
    location_id = serializers.IntegerField(write_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)

    class Meta:
        model = Event
        fields = ('event_time', 'location_id', 'location_name')

    def validate_event_time(self, value):
        if value <= datetime.now():
            raise serializers.ValidationError("Event time can't be in the past!")
        remaining_time = value - now()
        if remaining_time <= timedelta(hours=1):
            raise serializers.ValidationError("Reminders can only be set for events scheduled more than 1 hour.")
        return value

    def validate(self, attrs):
        location_obj = Location.objects.get(id=attrs.get('location_id'))
        weekday = attrs.get('event_time').strftime("%A")
        if not location_obj.working_hours:
            return attrs
        if weekday not in location_obj.working_hours:
            raise serializers.ValidationError('Reminder time should be in the working days!')
        else:
            opening_time, closing_time = (
                time.fromisoformat(location_obj.working_hours[weekday][0]),
                time.fromisoformat(location_obj.working_hours[weekday][1])
            )
            reminder_time = attrs.get('event_time').time()
            if not opening_time <= reminder_time <= closing_time:
                raise serializers.ValidationError('Reminder time should be within the working hours!')
        return attrs
