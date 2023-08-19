from enum import Enum
from rest_framework import serializers
from hackathon.models import Hackathon, Organiser
from user.models import User
from user.serializers import UserSerializer


class SubmissionTypeEnum(Enum):
    IMAGE = 'image'
    FILE = 'file'
    LINK = 'link'


class OrganiserAccessEnum(Enum):
    ADMIN = 0
    EDITOR = 1
    VIEWER = 2


class HackathonOrganiserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    access = serializers.ChoiceField(choices=[(access.value, access.name) for access in OrganiserAccessEnum], required=True)

    class Meta:
        model = Organiser
        fields = ('user', 'access')


class CreateHackathonOrganiserSerializer(HackathonOrganiserSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    class Meta:
        model = Organiser
        fields = ('user', 'access')


class HackathonSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    logo = serializers.ImageField(required=False)
    cover = serializers.ImageField(required=False)
    allowedSubmissions = serializers.ChoiceField(choices=[(submission.value, submission.name) for submission in SubmissionTypeEnum], required=True)
    minimumTeamSize = serializers.IntegerField(required=True)
    allowIndividual = serializers.BooleanField(required=True)
    startTimestamp = serializers.DateTimeField(required=True)
    endTimestamp = serializers.DateTimeField(required=True)
    pricePool = serializers.IntegerField(required=True)
    organisers = HackathonOrganiserSerializer(many=True, read_only=True, source='organiser_set')

    class Meta:
        model = Hackathon
        fields = '__all__'


class CreateHackathonSerializer(HackathonSerializer):
    organisers = CreateHackathonOrganiserSerializer(many=True, source='organiser_set')

    class Meta:
        model = Hackathon
        fields = '__all__'


class UpdateHackathonSerializer(CreateHackathonSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Hackathon
        fields = '__all__'


__all__ = [
    'HackathonSerializer',
    'UpdateHackathonSerializer',
    'CreateHackathonSerializer',
    'HackathonOrganiserSerializer',
    'CreateHackathonOrganiserSerializer',
]
