from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer
from .tasks import send_reminder
from celery import current_app
from datetime import timedelta
from django.utils.timezone import now, make_aware


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.prefetch_related('user', 'location').filter(user=self.request.user)

    def perform_create(self, serializer):
        event = serializer.save(user=self.request.user)
        # Calculate remaining time and schedule task
        remaining_time = event.event_time - now()
        if remaining_time > timedelta(hours=2):  # Reminder will be sent to user, if remaining time > 2 hours.
            alert_time = event.event_time - timedelta(hours=2)
            if alert_time.tzinfo is None:
                alert_time = make_aware(alert_time)

            task = send_reminder.apply_async(
                (event.user.email, event.location.city.name, event.location.name, event.event_time), eta=alert_time
            )
            event.alert_task_id = task.id  # saving alert_task_id give program to have control in case user decide to modify event_time or delete it, to terminate task process and not send email to user.
            event.save()

    def perform_update(self, serializer):
        event = serializer.save()
        if event.alert_task_id:
            current_app.control.revoke(event.alert_task_id, terminate=True)  # This will terminate process of sending reminder message to user, which means that the task located in redis broker won't be accomplished.

        # Schedule a new task if the remaining time > 2 hours
        remaining_time = event.event_time - now()
        if remaining_time > timedelta(hours=2):
            alert_time = event.event_time - timedelta(hours=2)
            if alert_time.tzinfo is None:
                alert_time = make_aware(alert_time)

            task = send_reminder.apply_async(
                (event.user.email, event.location.city, event.location.name, event.event_time), eta=alert_time
            )
            event.alert_task_id = task.id
        else:
            event.alert_task_id = None

        event.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.alert_task_id:
            current_app.control.revoke(instance.alert_task_id, terminate=True)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
