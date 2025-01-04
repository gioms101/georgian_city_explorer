from django.urls import path, include
from .views import (UserProfileViewSet, RegisterAPIView, ConfirmEmailView, ForgotPasswordRequestAPIView,
                    ResetPasswordAPIView)
from .custom_routers import CustomRouter

router = CustomRouter(trailing_slash=False)

router.register(r'profile', UserProfileViewSet)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('email-verify/<str:user_pk>/<str:token>/', ConfirmEmailView.as_view(), name='email-verify'),
    path('password-reset/', ForgotPasswordRequestAPIView.as_view(), name='request-reset'),
    path('password-reset/<str:user_pk>/<str:token>/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('', include(router.urls)),
]
