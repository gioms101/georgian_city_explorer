from django.urls import path, include
from .views import UserProfileViewSet, RegisterAPIView, ConfirmEmailView
from .custom_routers import CustomRouter

router = CustomRouter(trailing_slash=False)

router.register(r'profile', UserProfileViewSet)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('email-verify/<int:user_id>/<str:token>/', ConfirmEmailView.as_view(), name='email-verify'),
    path('', include(router.urls)),
]
