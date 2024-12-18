from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PossibleLocationViewSet

router = DefaultRouter()

router.register(r'locations', PossibleLocationViewSet)

urlpatterns = [
    path('', include(router.urls))
]
