from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'bio', 'avatar')


class DeleteProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('password',)


class UserQueryInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        fields = ('id',)
        extra_kwargs = {'id': {'required': True}}


__all__ = [
    'UserSerializer',
    'DeleteProfileSerializer',
    'UserQueryInputSerializer'
]
