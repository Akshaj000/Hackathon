from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from team.models import Team, TeamMember
from user.decorators import handle_refresh
from user.authentication import CookieTokenAuthentication
from team.serializers import TeamSerializer, CreateTeamSerializer, DeleteTeamSerializer, UpdateTeamSerializer
from team.decorators import extract_member_ids, resolve_team


class CreateTeamView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateTeamSerializer

    @extract_member_ids
    @handle_refresh
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        name = data.get('name')
        description = data.get('description')
        if not username:
            return Response({
                'error': {
                    'code': "USERNAME_REQUIRED",
                    'message': 'Username is required'
                },
            }, status=400)
        if Team.objects.filter(username=username).exists():
            return Response({
                'error': {
                    'code': "TEAM_ALREADY_EXISTS",
                    'message': 'Team already exists'
                },
            }, status=400)
        team = Team.objects.create(
            username=username,
            name=name,
            description=description
        )
        TeamMember.objects.create(
            user=request.user,
            team=team,
            isOwner=True
        )
        member_user_ids = self.member_ids
        if request.user.id in member_user_ids:
            member_user_ids.remove(request.user.id)
        for userID in member_user_ids:
            TeamMember.objects.create(
                user_id=userID,
                team=team
            )
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=200)


class UpdateTeamView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateTeamSerializer

    @resolve_team
    @handle_refresh
    def post(self, request, *args, **kwargs):
        data = request.data
        team = self.team
        if data.get('name'):
            team.name = data.get('name')
        if data.get('description'):
            team.description = data.get('description')
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=200)


class DeleteTeamView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteTeamSerializer

    @resolve_team
    @handle_refresh
    def post(self, request, *args, **kwargs):
        # TODO: Add more logic incase the team is already registered for a hackathon
        user = request.user
        data = request.data
        user_password = data.get('password')
        team = self.team
        if not user.check_password(user_password):
            return Response({
                'error': {
                    'code': 'INVALID_PASSWORD',
                    'message': 'Invalid password'
                }
            }, status=400)
        team.delete()
        return Response({}, status=200)


__all__ = [
    'CreateTeamView',
    'DeleteTeamView',
    'UpdateTeamView'
]
