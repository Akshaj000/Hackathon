from rest_framework.response import Response
from rest_framework.views import APIView

from hackathon.models import Submission
from user.decorators import handle_refresh
from hackathon.models import Evaluation


class EvaluateSubmissionView(APIView):

    @handle_refresh
    def post(self, request, *args, **kwargs):
        data = request.data
        submissionID = data.get('submissionID')
        review = data.get('review')
        score = data.get('score')

        for fields in [submissionID, review, score]:
            if not fields:
                return Response({
                    'error': {
                        'code': 'FIELD_REQUIRED',
                        'message': 'All fields are required'
                    }
                }, status=400)

        if not Submission.objects.filter(id=submissionID).exists():
            return Response({
                'error': {
                    'code': 'INVALID_SUBMISSION_ID',
                    'message': 'Invalid submission ID'
                }
            }, status=400)

        evaluation = Evaluation.objects.create(
            submission_id=submissionID,
            review=review,
            score=score,
            evaluator=request.user
        )

        return Response({
            'message': 'Successfully evaluated'
        }, status=200)


__all__ = [
    'EvaluateSubmissionView'
]
