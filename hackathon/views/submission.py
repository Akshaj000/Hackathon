from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from hackathon.decorators import resolve_hackathon
from hackathon.models import Submission, Hackathon, Registration
from user.authentication import CookieTokenAuthentication
from user.decorators import handle_refresh
from hackathon.serializers import SubmissionInputSerializer, SubmissionOutputSerializer, GetHackathonInputSerializer


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
        if hackathon.submission_set.filter(user=request.user).exists():
            return Response({
                'error': {
                    'code': 'ALREADY_SUBMITTED',
                    'message': 'You have already submitted your project'
                }
            }, status=400)
        if not registration.exists():
            return Response({
                'error': {
                    'code': 'NOT_REGISTERED',
                    'message': 'You are not registered for this hackathon'
                }
            }, status=400)
        registration = registration.first()
        if registration.hackathon.allowedSubmissionType == "file" and not file:
            return Response({
                'error': {
                    'code': 'MISSING_FIELD',
                    'message': 'file is required'
                }
            }, status=400)
        if registration.hackathon.allowedSubmissionType == "link" and not link:
            return Response({
                'error': {
                    'code': 'MISSING_FIELD',
                    'message': 'link is required'
                }
            }, status=400)
        if registration.hackathon.allowedSubmissionType == "image" and not image:
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
        if registration.hackathon.allowedSubmissionType == "file":
            submission.file = file
        if registration.hackathon.allowedSubmissionType == "link":
            submission.link = link
        if registration.hackathon.allowedSubmissionType == "image":
            submission.image = image
        if summary:
            submission.summary = summary
        submission.save()
        return Response(SubmissionOutputSerializer(submission).data, status=200)


class SubmissionsView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @handle_refresh
    @resolve_hackathon("viewer")
    def get(self, request):
        hackathon = self.hackathon
        submissions = Submission.objects.filter(hackathon=hackathon)
        return Response(SubmissionOutputSerializer(submissions, many=True).data, status=200)


class MySubmissionsView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetHackathonInputSerializer

    @handle_refresh
    def post(self, request):
        data = request.data
        if 'id' not in data and data['id'] is None:
            return Response({
                'error': {
                    'code': 'MISSING_FIELD',
                    'message': 'hackathonID is required'
                }
            }, status=400)
        submissions = Submission.objects.filter(
            hackathon_id=data['id']
        )
        return Response(SubmissionOutputSerializer(submissions, many=True).data, status=200)


__all__ = [
    'CreateSubmissionView',
    'SubmissionsView',
    'MySubmissionsView'
]
