from rest_framework import serializers

from team.models import Team
from team.serializers.teamMember import TeamMemberSerializer
from user.models import User


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=False, read_only=True)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    members = TeamMemberSerializer(many=True, read_only=True, source='teammember_set')

    class Meta:
        model = Team
        fields = ('id', 'username', 'name', 'description', 'members')


class CreateTeamSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    members = serializers.ListSerializer(child=serializers.IntegerField(), required=True)

    class Meta:
        model = Team
        fields = ('username', 'name', 'description',  'members')


class UpdateTeamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Team
        fields = ('id', 'name', 'description')


class DeleteTeamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = Team
        fields = ('id', 'password')


__all__ = [
    'TeamSerializer',
    'TeamMemberSerializer',
    'CreateTeamSerializer',
    'UpdateTeamSerializer',
    'DeleteTeamSerializer'
]
