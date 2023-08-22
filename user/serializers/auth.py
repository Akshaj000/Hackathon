from django.db.models import Q
from rest_framework import serializers

from user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _


class UserLoginSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def validate(self, attrs):
        username_or_email = attrs.get(self.username_field)
        password = attrs.get('password')

        if not username_or_email or not password:
            raise serializers.ValidationError(_('Both username/email and password are required.'), code='invalid_credentials')

        try:
            user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
        except User.DoesNotExist:
            raise serializers.ValidationError(self.error_messages['no_active_account'], code='no_active_account')

        if not user.is_active:
            raise serializers.ValidationError(self.error_messages['no_active_account'], code='no_active_account')
        if user.is_banned:
            raise serializers.ValidationError(_('Your account has been banned.'), code='banned_account')
        if not user.check_password(password):
            raise serializers.ValidationError(self.error_messages['no_active_account'], code='no_active_account')
        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'name')
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.avatar:
            representation['avatar'] = None
        return representation

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


__all__ = [
    'UserRegistrationSerializer',
    'UserLoginSerializer'
]
