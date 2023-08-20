from enum import Enum
from rest_framework import serializers
from hackathon.models import Hackathon
from hackathon.serializers.organizer import OrganiserInputSerializer, OrganiserOutputSerializer


class SubmissionTypeEnum(Enum):
    IMAGE = 'image'
    FILE = 'file'
    LINK = 'link'


class HackathonOutputSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    logo = serializers.ImageField(required=False)
    cover = serializers.ImageField(required=False)
    allowedSubmissionType = serializers.ChoiceField(choices=[(submission.value, submission.name) for submission in SubmissionTypeEnum], required=True)
    minimumTeamSize = serializers.IntegerField(required=True)
    allowIndividual = serializers.BooleanField(required=True)
    startTimestamp = serializers.DateTimeField(required=True)
    endTimestamp = serializers.DateTimeField(required=True)
    pricePool = serializers.IntegerField(required=True)
    organisers = OrganiserOutputSerializer(many=True, read_only=True, source='organiser_set')

    class Meta:
        model = Hackathon
        fields = '__all__'


class CreateHackathonInputSerializer(HackathonOutputSerializer):
    organisers = OrganiserInputSerializer(many=True, source='organiser_set')

    class Meta:
        model = Hackathon
        fields = '__all__'


class UpdateHackathonInputSerializer(CreateHackathonInputSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Hackathon
        fields = '__all__'


class DeleteHackathonInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        fields = '__all__'


__all__ = [
    'HackathonOutputSerializer',
    'UpdateHackathonInputSerializer',
    'CreateHackathonInputSerializer',
    'DeleteHackathonInputSerializer'
]
