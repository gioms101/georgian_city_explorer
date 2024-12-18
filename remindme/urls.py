from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet

router = DefaultRouter()

router.register(r'reminder', EventViewSet, basename='reminder')

urlpatterns = [
    path('', include(router.urls)),
]

