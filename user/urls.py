from django.urls import path, include
from .views import UserProfileViewSet
from .custom_routers import CustomRouter

router = CustomRouter(trailing_slash=False)

router.register(r'profile', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
