from enum import Enum

from rest_framework import serializers

from hackathon.models import Organiser
from user.models import User
from user.serializers import UserSerializer


class OrganiserAccessEnum(Enum):
    ADMIN = 0
    EDITOR = 1
    VIEWER = 2


class OrganiserOutputSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    access = serializers.ChoiceField(choices=[(access.value, access.name) for access in OrganiserAccessEnum], required=True)

    class Meta:
        model = Organiser
        fields = ('user', 'access')


class OrganiserInputSerializer(OrganiserOutputSerializer):
    userID = serializers.IntegerField(required=True)
    access = serializers.ChoiceField(choices=[(access.value, access.name) for access in OrganiserAccessEnum], required=True)

    class Meta:
        model = Organiser
        fields = ('userID', 'access')


__all__ = [
    'OrganiserInputSerializer',
    'OrganiserOutputSerializer',
]
