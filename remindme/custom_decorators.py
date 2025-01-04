from django.utils.timezone import make_aware
from datetime import timedelta
from .tasks import send_reminder


def send_alert(func):
    def wrapper(self, serializer, *args, **kwargs):
        event = func(self, serializer, *args, **kwargs)
        alert_time = event.event_time - timedelta(hours=1)
        if alert_time.tzinfo is None:
            alert_time = make_aware(alert_time)
        task = send_reminder.apply_async(
                (event.id, event.user.email, event.location.city.name, event.location.name, event.event_time),
                eta=alert_time
            )
        event.alert_task_id = task.id
        event.save()
        return event
    return wrapper
