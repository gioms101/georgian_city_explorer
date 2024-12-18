from django.db import models
from user.models import CustomUser
from main.models import Location


# Create your models here.

class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    event_time = models.DateTimeField()
    alert_task_id = models.CharField(max_length=255, blank=True, null=True)  # This is used to control deleting and updating Event object.
