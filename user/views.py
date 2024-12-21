from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import RegisterUserSerializer, UserProfileSerializer, ChangePasswordSerializer
from .models import CustomUser


# Create your views here.


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterUserSerializer


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
