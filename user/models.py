from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='pics/', default='default.png')
    email = models.EmailField(unique=True, blank=False)
    is_verified = models.BooleanField(default=False)
