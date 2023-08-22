from rest_framework import serializers

from team.models import Team, TeamMember
from user.serializers import UserSerializer


class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TeamMember
        fields = ('user', 'isOwner')


class UpdateTeamMemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    members = serializers.ListSerializer(child=serializers.IntegerField(), required=True)

    class Meta:
        model = Team
        fields = ('id', 'members')


class TeamGetInputSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Team
        fields = ('id',)


class TransferOwnershipSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    userID = serializers.IntegerField(required=True)

    class Meta:
        model = Team
        fields = ('id', 'userID')


__all__ = [
    'TeamMemberSerializer',
    'UpdateTeamMemberSerializer',
    'TeamGetInputSerializer',
    'TransferOwnershipSerializer'
]
