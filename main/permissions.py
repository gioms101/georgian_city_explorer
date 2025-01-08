from django.utils.timezone import now
from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class HasActiveSubscription(permissions.BasePermission):
    message = "You don't have active subscription!"

    def has_permission(self, request, view):
        subscriptions = request.user.subscription.all()
        for subscription in subscriptions:
            if subscription.expiration_date > now():
                return True
        return False
