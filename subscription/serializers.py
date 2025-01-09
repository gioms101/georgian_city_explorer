from rest_framework import serializers
from .models import SubscriptionPlan


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        exclude = ('plan_id',)


class SubscriptionSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()

class CompleteSubscriptionSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
