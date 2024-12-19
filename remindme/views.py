from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer
from .custom_decorators import send_alert
from celery import current_app


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.prefetch_related('user', 'location').filter(user=self.request.user)

    @send_alert
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @send_alert
    def perform_update(self, serializer):
        event = serializer.save()
        if event.alert_task_id:
            current_app.control.revoke(event.alert_task_id, terminate=True)
        return event

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.alert_task_id:
            current_app.control.revoke(instance.alert_task_id, terminate=True)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
