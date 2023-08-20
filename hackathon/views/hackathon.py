from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from hackathon.decorators import resolve_hackathon
from hackathon.models import Hackathon, Organiser
from user.authentication import CookieTokenAuthentication
from hackathon.serializers import HackathonOutputSerializer, CreateHackathonInputSerializer, DeleteHackathonInputSerializer
from user.decorators import handle_refresh
from user.models import User


class PublishHackathonView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateHackathonInputSerializer

    @handle_refresh
    def post(self, request, *args, **kwargs):

        data = request.data
        for fields in ["title", "description", "allowedSubmissionType", "startTimestamp", "endTimestamp", "pricePool"]:
            if not data.get(fields):
                return Response({
                    'error': {
                        'code': 'MISSING_FIELD',
                        'message': f'{fields} is required'
                    }
                }, status=400)
        if not (data.get('maximumTeamSize') and data.get('minimumTeamSize')) and data.get('allowIndividual'):
            return Response({
                'error': {
                    'code': 'MISSING_FIELD',
                    'message': 'teamSizes or allowIndividual is required'
                }
            }, status=400)

        # Create hackathon
        hackathon = Hackathon.objects.create(
            title=data.get('title'),
            description=data.get('description'),
            allowedSubmissions=data.get('allowedSubmissions'),
            maximumTeamSize=data.get('maximumTeamSize', 0),
            minimumTeamSize=data.get('minimumTeamSize', 0),
            allowIndividual=data.get('allowIndividual', False),
            startTimestamp=data.get('startTimestamp'),
            endTimestamp=data.get('endTimestamp'),
            pricePool=data.get('pricePool'),
        )
        if "logo" in data and data.get('logo'):
            hackathon.logo = data.get('logo')
        if "cover" in data and data.get('cover'):
            hackathon.cover = data.get('cover')
        # Create organiser for the hackathon
        Organiser.objects.create(
            user=request.user,
            hackathon=hackathon,
            access=0
        )
        if data.get('organisers'):
            if User.objects.filter(id__in=[organiser.get('userID') for organiser in data.get('organisers')]).count() != len(data.get('organisers')):
                return Response({
                    'error': {
                        'code': 'INVALID_USER',
                        'message': 'Invalid user ID'
                    }
                }, status=400)
            for organiser in data.get('organisers'):
                if organiser.get('userID') == request.user.id:
                    continue
                Organiser.objects.create(
                    user_id=organiser.get('userID'),
                    hackathon=hackathon,
                    access=organiser.get('access')
                )
        hackathon.save()
        serializer = HackathonOutputSerializer(hackathon)
        return Response(serializer.data, status=200)


class UpdateHackathonView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateHackathonInputSerializer

    @handle_refresh
    @resolve_hackathon("editor")
    def post(self, request, *args, **kwargs):
        data = request.data
        hackathon = self.hackathon
        if data.get('title'):
            hackathon.title = data.get('title')
        if data.get('description'):
            hackathon.description = data.get('description')
        if data.get('logo'):
            hackathon.logo = data.get('logo')
        if data.get('cover'):
            hackathon.cover = data.get('cover')
        if data.get('allowedSubmissionType'):
            hackathon.allowedSubmissionType = data.get('allowedSubmissionType')
        if data.get('minimumTeamSize'):
            hackathon.minimumTeamSize = data.get('minimumTeamSize')
        if data.get('allowIndividual'):
            hackathon.allowIndividual = data.get('allowIndividual')
        if data.get('startTimestamp'):
            hackathon.startTimestamp = data.get('startTimestamp')
        if data.get('endTimestamp'):
            hackathon.endTimestamp = data.get('endTimestamp')
        if data.get('pricePool'):
            hackathon.pricePool = data.get('pricePool')
        hackathon.save()
        serializer = HackathonOutputSerializer(hackathon)
        return Response(serializer.data, status=200)


class DeleteHackathonView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteHackathonInputSerializer

    @handle_refresh
    @resolve_hackathon("admin")
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        user_password = data.get('password')
        hackathon = self.hackathon
        if not user.check_password(user_password):
            return Response({
                'error': {
                    'code': 'INVALID_PASSWORD',
                    'message': 'Invalid password'
                }
            }, status=400)
        hackathon.delete()
        return Response(status=200)


__all__ = [
    'PublishHackathonView',
    'UpdateHackathonView',
    'DeleteHackathonView'
]
