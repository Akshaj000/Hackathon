from rest_framework import serializers

from hackathon.models import Registration
from user.serializers import UserSerializer
from team.serializers import TeamSerializer
from hackathon.serializers import HackathonOutputSerializer


class RegistrationOutputSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    hackathon = HackathonOutputSerializer(read_only=True)
    timeStampRegistered = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ('user', 'team', 'hackathon', 'timestampRegistered')


class RegistrationInputSerializer(RegistrationOutputSerializer):
    teamID = serializers.IntegerField(required=False)
    hackathonID = serializers.IntegerField(required=True)

    class Meta:
        model = Registration
        fields = ('teamID', 'hackathonID')
        read_only_fields = ('user', 'team', 'hackathon', 'timestampRegistered')


__all__ = [
    'RegistrationOutputSerializer',
    'RegistrationInputSerializer'
]
