from django.shortcuts import get_object_or_404
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
from .serializers import RegisterUserSerializer, UserProfileSerializer, ChangePasswordSerializer
from .models import CustomUser
from .tasks import send_email_verification


# Create your views here.


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        token = default_token_generator.make_token(user)
        link = self.request.build_absolute_uri(
            reverse('email-verify', kwargs={'user_id': user.id, 'token': token})
        )
        send_email_verification.delay(user.email, link)


class ConfirmEmailView(APIView):
    serializer_class = None

    def get(self, request, user_id, token):
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

