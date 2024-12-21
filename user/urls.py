from django.urls import path, include
from .views import UserProfileViewSet, RegisterAPIView
from .custom_routers import CustomRouter

router = CustomRouter(trailing_slash=False)

router.register(r'profile', UserProfileViewSet)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('', include(router.urls)),
]
