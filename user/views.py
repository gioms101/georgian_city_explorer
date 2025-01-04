from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (RegisterUserSerializer, UserProfileSerializer, ChangePasswordSerializer,
                          ForgotPasswordRequestSerializer, ResetPasswordSerializer)
from .models import CustomUser
from .tasks import send_email_verification, reset_password


# Create your views here.


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = self.request.build_absolute_uri(
            reverse('email-verify', kwargs={'user_pk': encoded_pk, 'token': token})
        )
        send_email_verification.delay(user.email, link)


class ConfirmEmailView(APIView):
    serializer_class = None

    def get(self, request, user_pk, token):
        user_id = urlsafe_base64_decode(user_pk).decode()
        user = get_object_or_404(CustomUser, id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save(update_fields=['is_verified'])
            return Response({'message': 'Email verified successfully!'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'change_password':
            return ChangePasswordSerializer
        return UserProfileSerializer

    def get_object(self):
        return self.request.user

    @action(detail=False, methods=['patch'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])
        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)


class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = CustomUser.objects.get(username=request.data['username'])
        if not user.is_verified:
            return Response({'error': 'Email not verified'}, status=status.HTTP_403_FORBIDDEN)
        return response


class ForgotPasswordRequestAPIView(APIView):
    serializer_class = ForgotPasswordRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(email=serializer.validated_data['email'])
        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        url_link = self.request.build_absolute_uri(
            reverse('reset-password', kwargs={'user_pk': encoded_pk, 'token': token})
        )
        reset_password.delay(user.email, url_link)
        return Response({"message": "The reset link has been sent on your email!"}, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_pk = urlsafe_base64_decode(kwargs.get('user_pk')).decode()
        user = CustomUser.objects.get(pk=user_pk)
        if not PasswordResetTokenGenerator().check_token(user, kwargs.get('token')):
            return Response({'message': "Invalid token!"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])
        return Response({"message": "Your password has been changed successfully!"}, status=status.HTTP_200_OK)
