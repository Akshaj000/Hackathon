from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from hackathon.models import Submission, Hackathon, Registration
from user.authentication import CookieTokenAuthentication
from user.decorators import handle_refresh
from hackathon.serializers import SubmissionInputSerializer, SubmissionOutputSerializer


class CreateSubmissionView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionInputSerializer

    @handle_refresh
    def post(self, request):
        data = request.data
        hackathonID = data.get('hackathonID')
        file = data.get('file')
        link = data.get('link')
        image = data.get('image')
        summary = data.get('summary')
        try:
            hackathon = Hackathon.objects.get(id=hackathonID)
        except Hackathon.DoesNotExist:
            return Response({
                'error': {
                    'code': 'HACKATHON_NOT_FOUND',
                    'message': 'Hackathon not found'
                }
            }, status=404)
        registration = Registration.objects.filter(
            Q(hackathon=hackathon) & Q(Q(user=request.user) | Q(team__teammember__user=request.user))
        )
        if not registration.exists():
            return Response({
                'error': {
                    'code': 'NOT_REGISTERED',
                    'message': 'You are not registered for this hackathon'
                }
            }, status=400)
        registration = registration.first()
        if registration.hackathon.allowedSubmissions == "file" and not file:
            return Response({
                'error': {
                    'code': 'MISSING_FIELD',
                    'message': 'file is required'
                }
            }, status=400)
        if registration.hackathon.allowedSubmissions == "link" and not link:
            return Response({
                'error': {
                    'code': 'MISSING_FIELD',
                    'message': 'link is required'
                }
            }, status=400)
        if registration.hackathon.allowedSubmissions == "image" and not image:
            return Response({
                'error': {
                    'code': 'MISSING_FIELD',
                    'message': 'image is required'
                }
            }, status=400)
        submission = Submission.objects.create(
            hackathon_id=hackathonID,
            user=request.user,
            team=registration.team
        )
        if registration.hackathon.allowedSubmissions == "file":
            submission.file = file
        if registration.hackathon.allowedSubmissions == "link":
            submission.link = link
        if registration.hackathon.allowedSubmissions == "image":
            submission.image = image
        if summary:
            submission.summary = summary
        submission.save()
        return Response({
            'message': 'Successfully submitted'
        }, status=200)


__all__ = [
    'CreateSubmissionView'
]
