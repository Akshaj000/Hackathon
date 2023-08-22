from rest_framework import serializers

from hackathon.models import Submission, Evaluation
from team.serializers import TeamSerializer
from user.serializers import UserSerializer


class EvaluationOutputSerializer(serializers.ModelSerializer):
    evaluator = UserSerializer(read_only=True)
    review = serializers.CharField(required=True)
    score = serializers.IntegerField(required=True)
    timeStampEvaluated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Evaluation
        fields = '__all__'
        read_only_fields = ('evaluator', 'review', 'score', 'timeStampEvaluated')


class EvaluationInputSerializer(EvaluationOutputSerializer):
    submissionID = serializers.IntegerField(required=True)

    class Meta:
        model = Evaluation
        fields = ('submissionID', 'review', 'score')
        read_only_fields = ('evaluator', 'timeStampEvaluated')


class SubmissionOutputSerializer(serializers.ModelSerializer):
    idc = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    file = serializers.FileField(read_only=True)
    link = serializers.URLField(read_only=True)
    image = serializers.ImageField(read_only=True)
    summary = serializers.CharField(read_only=True)
    timestampSubmitted = serializers.DateTimeField(read_only=True)
    evaluations = EvaluationOutputSerializer(many=True, read_only=True, source='evaluation_set')

    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ('id', 'user', 'team', 'file', 'link', 'image', 'summary', 'timestampSubmitted', 'evaluations')


class SubmissionInputSerializer(SubmissionOutputSerializer):
    teamID = serializers.IntegerField(required=False)
    hackathonID = serializers.IntegerField(required=True)
    file = serializers.FileField(required=False)
    image = serializers.ImageField(required=False)
    link = serializers.URLField(required=False)
    summary = serializers.CharField(required=False)

    class Meta:
        model = Submission
        fields = ('teamID', 'hackathonID', 'file', 'image', 'link', 'summary')
        read_only_fields = ('user', 'team', 'timestampSubmitted')


__all__ = [
    'SubmissionOutputSerializer',
    'SubmissionInputSerializer',
    'EvaluationOutputSerializer',
    'EvaluationInputSerializer'
]
