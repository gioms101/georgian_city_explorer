from django.db import models
from django.template.defaultfilters import slugify

from main.models import Category, City
from user.models import CustomUser


# Create your models here.

class PossibleLocation(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # This field is used for possible map integration
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # This field is used for possible map integration
    image = models.ImageField(upload_to='loc_pics/')
    working_hours = models.JSONField(default=dict, blank=True)
    description = models.TextField(blank=True, null=True)
    votes = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return self.name
