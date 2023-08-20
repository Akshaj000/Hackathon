from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from hackathon.models import Registration, Hackathon
from team.models import Team
from user.authentication import CookieTokenAuthentication
from user.decorators import handle_refresh
from hackathon.serializers import RegistrationInputSerializer, RegistrationOutputSerializer


class CreateRegistrationView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RegistrationInputSerializer

    @handle_refresh
    def post(self, request):
        data = request.data
        hackathonID = data.get('hackathonID')
        teamID = data.get('teamID')
        try:
            hackathon = Hackathon.objects.get(id=hackathonID)
        except Hackathon.DoesNotExist:
            return Response({
                'error': {
                    'code': 'HACKATHON_NOT_FOUND',
                    'message': 'Hackathon not found'
                }
            }, status=404)
        if hackathon.endTimestamp < hackathon.startTimestamp:
            return Response({
                'error': {
                    'code': 'INVALID_HACKATHON',
                    'message': 'Hackathon has ended'
                }
            }, status=400)
        if teamID is None and not hackathon.allowIndividual:
            return Response({
                'error': {
                    'code': 'INVALID_HACKATHON',
                    'message': 'Hackathon does not allow individual submission'
                }
            }, status=400)
        if teamID is not None and hackathon.minimumTeamSize < 1:
            return Response({
                'error': {
                    'code': 'INVALID_HACKATHON',
                    'message': 'Hackathon does not allow team submission'
                }
            }, status=400)
        if teamID is not None:
            try:
                team = Team.objects.get(id=teamID)
            except Team.DoesNotExist:
                return Response({
                    'error': {
                        'code': 'TEAM_NOT_FOUND',
                        'message': 'Team not found'
                    }
                }, status=404)
            if team.teammember_set.count() < hackathon.minimumTeamSize:
                return Response({
                    'error': {
                        'code': 'INVALID_TEAM',
                        'message': 'Team does not meet minimum team size'
                    }
                }, status=400)
            if not team.teammember_set.filter(user=request.user, isOwner=True).exists():
                return Response({
                    'error': {
                        'code': 'INVALID_TEAM',
                        'message': 'User is not team owner to register'
                    }
                }, status=400)
        registration = Registration.objects.create(
            hackathon_id=hackathonID,
            user=request.user,
        )
        if teamID:
            registration.team_id = teamID
            registration.save()
        return Response(RegistrationOutputSerializer(registration).data, status=200)


__all__ = [
    'CreateRegistrationView'
]

