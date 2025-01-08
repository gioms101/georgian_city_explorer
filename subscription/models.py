from django.db import models
from user.models import CustomUser


# Create your models here.

class SubscriptionPlan(models.Model):
    CURRENCY = [
        ("USD", "USD"),
        ("EUR", "EUR"),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="Enter the duration in months")
    price = models.IntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY)
    plan_id = models.CharField(max_length=100, unique=True, null=True, blank=True, help_text="Don't fill this field, This is automatically generated when created")  # PayPal Plan ID

    def __str__(self):
        return self.name

class Subscription(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="subscription")
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Subscription."
