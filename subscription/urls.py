from django.urls import path
from .views import (CreateSubscriptionPlanAPIView, CreateSubscriptionAPIView, SuccessResponseView,
                    CancelSubscriptionAPIView, CompleteSubscriptionAPIView)

urlpatterns = [
    path('create-plan/', CreateSubscriptionPlanAPIView.as_view(), name='create-plan'),
    path('create-subscription/', CreateSubscriptionAPIView.as_view(), name='create-subscription'),
    path('complete-subscription/', CompleteSubscriptionAPIView.as_view(), name='complete-subscription'),
    path('success/', SuccessResponseView.as_view(), name='success'),
    path('cancel/', CancelSubscriptionAPIView.as_view(), name='cancel'),
]
