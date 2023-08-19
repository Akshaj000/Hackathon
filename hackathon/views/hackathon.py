from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from hackathon.models import Hackathon, Organiser
from user.authentication import CookieTokenAuthentication
from hackathon.serializers import HackathonSerializer, CreateHackathonSerializer
from user.decorators import handle_refresh
from user.models import User


class CreateHackathonView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateHackathonSerializer

    @handle_refresh
    def post(self, request, *args, **kwargs):

        data = request.data
        title = data.get('title')
        description = data.get('description')
        logo = data.get('logo')
        cover = data.get('cover')
        allowedSubmissionType = data.get('allowedSubmissionType')
        minimumTeamSize = data.get('minimumTeamSize')
        allowIndividual = data.get('allowIndividualSubmission')
        startTimestamp = data.get('startTimestamp')
        endTimestamp = data.get('endTimestamp')
        pricePool = data.get('pricePool')
        organisers = data.get('organisers')

        for fields in [title, description, allowedSubmissionType, minimumTeamSize, allowIndividual, startTimestamp, endTimestamp, pricePool]:
            if not fields:
                return Response({
                    'error': {
                        'code': 'FIELD_REQUIRED',
                        'message': 'All fields are required'
                    }
                }, status=400)

        hackathon = Hackathon.objects.create(
            title=title,
            description=description,
            allowedSubmissionType=allowedSubmissionType,
            minimumTeamSize=minimumTeamSize,
            allowIndividual=allowIndividual,
            startTimestamp=startTimestamp,
            endTimestamp=endTimestamp,
            pricePool=pricePool
        )
        if logo:
            hackathon.logo = logo
        if cover:
            hackathon.cover = cover
        Organiser.objects.create(
            user=request.user,
            hackathon=hackathon,
            access='admin'
        )
        if request.user.id in [organiser.userID for organiser in organisers]:
            element = organisers.pop([organiser.userID for organiser in organisers].index(request.user.id))
            organisers.remove(element)
        for organiser in organisers:
            if not User.objects.filter(username=organiser.username).exists():
                return Response({
                    'error': {
                        'code': 'USER_NOT_FOUND',
                        'message': 'User not found'
                    }
                }, status=400)
            Organiser.objects.create(
                user_id=organiser.userID,
                hackathon=hackathon,
                access=organiser.access
            )
        hackathon.save()
        serializer = HackathonSerializer(hackathon)
        return Response(serializer.data, status=200)


class UpdateHackathonView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateHackathonSerializer

    @handle_refresh
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
        serializer = HackathonSerializer(hackathon)
        return Response(serializer.data, status=200)


class DeleteHackathonView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @handle_refresh
    def post(self, request, *args, **kwargs):
        hackathon = self.hackathon
        hackathon.delete()
        return Response(status=200)


__all__ = [
    'CreateHackathonView',
]
