from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .tasks import send_email_verification
from .models import CustomUser


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     validators=[validate_password],
                                     )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'image')

    def save(self, **kwargs):
        instance = super().save(**kwargs)

        if 'email' in self.validated_data:
            request = self.context.get('request')
            instance.is_verified = False
            instance.save(update_fields=['is_verified'])
            token = default_token_generator.make_token(instance)
            link = request.build_absolute_uri(
                reverse('email-verify', kwargs={'user_id': instance.id, 'token': token})
            )
            send_email_verification.delay(instance.email, link)
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

