from rest_framework import serializers

from team.models import Team, TeamMember
from user.models import User
from user.serializers import UserSerializer


class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TeamMember
        fields = ('user', 'isOwner')


class UpdateTeamMemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

    class Meta:
        model = Team
        fields = ('id', 'members')


__all__ = [
    'TeamMemberSerializer',
    'UpdateTeamMemberSerializer'
]
