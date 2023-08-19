from rest_framework.response import Response
from rest_framework.views import APIView

from hackathon.models import Registration
from user.decorators import handle_refresh


class Register(APIView):

    @handle_refresh
    def post(self, request):
        data = request.data
        hackathonID = data.get('hackathonID')
        teamID = data.get('teamID')
        registration = Registration.objects.create(
            hackathon_id=hackathonID,
            user=request.user,
        )
        if teamID:
            registration.team_id = teamID
            registration.save()
        return Response({
            'message': 'Successfully registered'
        }, status=200)


__all__ = [
    'Register'
]

