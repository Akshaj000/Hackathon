from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from hackathon.models import Submission
from user.authentication import CookieTokenAuthentication
from user.decorators import handle_refresh
from hackathon.models import Evaluation
from hackathon.serializers import EvaluationInputSerializer, SubmissionOutputSerializer


class EvaluateSubmissionView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EvaluationInputSerializer

    @handle_refresh
    def post(self, request, *args, **kwargs):
        data = request.data
        for fields in ["submissionID", "review", "score"]:
            if not fields in data:
                return Response({
                    'error': {
                        'code': 'MISSING_FIELD',
                        'message': f'{fields} is required'
                    }
                }, status=400)
        try:
            submission = Submission.objects.get(id=data['submissionID'])
        except Submission.DoesNotExist:
            return Response({
                'error': {
                    'code': 'SUBMISSION_NOT_FOUND',
                    'message': 'Submission not found'
                }
            }, status=404)
        if not submission.hackathon.organiser_set.filter(user=request.user, access__in=[0]).exists():
            return Response({
                'error': {
                    'code': 'PERMISSION_DENIED',
                    'message': 'You do not have permission to evaluate this submission'
                }
            }, status=400)
        Evaluation.objects.create(
            submission_id=data['submissionID'],
            review=data['review'],
            score=data['score'],
            evaluator=request.user
        )
        return Response(SubmissionOutputSerializer(submission).data, status=200)


class UpdateEvaluationView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EvaluationInputSerializer

    @handle_refresh
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            evaluation = Evaluation.objects.get(submission_id=data['submissionID'])
        except Evaluation.DoesNotExist:
            return Response({
                'error': {
                    'code': 'EVALUATION_NOT_FOUND',
                    'message': 'Evaluation not found'
                }
            }, status=404)
        if not evaluation.submission.hackathon.organiser_set.filter(user=request.user, access__in=[0]).exists():
            return Response({
                'error': {
                    'code': 'PERMISSION_DENIED',
                    'message': 'You do not have permission to evaluate this submission'
                }
            }, status=400)
        if data.get('review'):
            evaluation.review = data['review']
        if data.get('score'):
            evaluation.score = data['score']
        evaluation.save()
        return Response(SubmissionOutputSerializer(evaluation.submission).data, status=200)


__all__ = [
    'EvaluateSubmissionView',
    'UpdateEvaluationView'
]
