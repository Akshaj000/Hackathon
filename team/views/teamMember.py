from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from team.models import TeamMember
from user.decorators import handle_refresh
from user.models import User
from user.authentication import CookieTokenAuthentication
from team.serializers import TeamSerializer, UpdateTeamMemberSerializer, TeamGetInputSerializer, \
    TransferOwnershipSerializer
from team.decorators import resolve_team, extract_member_ids


class AddTeamMembersView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateTeamMemberSerializer

    @resolve_team
    @extract_member_ids
    @handle_refresh
    def post(self, request, *args, **kwargs):
        data = request.data
        team = self.team
        if not team.teammember_set.filter(user=request.user, isOwner=True).exists():
            return Response({
                'error': {
                    'code': "NOT_TEAM_OWNER",
                    'message': 'You are not the team owner. Only team owner can add members'
                },
            }, status=400)
        members = data.get('members')
        if not members:
            return Response({
                'error': {
                    'code': "MEMBERS_REQUIRED",
                    'message': 'Members are required'
                },
            }, status=400)

        member_user_ids = self.member_ids
        if request.user.id in member_user_ids:
            return Response({
                'error': {
                    'code': "CANNOT_ADD_SELF",
                    'message': 'Cannot add self to team'
                },
            }, status=400)
        if User.objects.filter(id__in=member_user_ids).count() != len(member_user_ids):
            return Response({
                'error': {
                    'code': "USER_NOT_FOUND",
                    'message': 'One or more users are not found'
                },
            }, status=400)
        if team.teammember_set.filter(user_id__in=member_user_ids).exists():
            return Response({
                'error': {
                    'code': "USER_ALREADY_IN_TEAM",
                    'message': 'One or more users are already in the team'
                },
            }, status=400)
        for userID in member_user_ids:
            TeamMember.objects.create(
                user_id=userID,
                team=team
            )
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=200)


class RemoveTeamMembersView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateTeamMemberSerializer

    @resolve_team
    @handle_refresh
    @extract_member_ids
    def post(self, request, *args, **kwargs):
        team = self.team
        if not team.teammember_set.filter(user=request.user, isOwner=True).exists():
            return Response({
                'error': {
                    'code': "NOT_TEAM_OWNER",
                    'message': 'Only team owner can remove members'
                },
            }, status=400)
        if not self.member_ids:
            return Response({
                'error': {
                    'code': "MEMBERS_REQUIRED",
                    'message': 'Members are required'
                },
            }, status=400)
        if request.user.id in self.member_ids:
            return Response({
                'error': {
                    'code': "CANNOT_REMOVE_SELF",
                    'message': 'Cannot remove self from team'
                },
            }, status=400)
        remove_member_list = self.member_ids
        for user_id in remove_member_list:
            try:
                TeamMember.objects.get(user_id=user_id, team=team).delete()
            except TeamMember.DoesNotExist:
                return Response({
                    'error': {
                        'code': "USER_NOT_IN_TEAM",
                        'message': 'User is not in the team'
                    },
                }, status=400)
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=200)


class LeaveTeamView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TeamGetInputSerializer

    @resolve_team
    @handle_refresh
    def post(self, request, *args, **kwargs):
        team = self.team
        if team.teammember_set.filter(user=request.user, isOwner=True).exists():
            return Response({
                'error': {
                    'code': "CANNOT_LEAVE_TEAM",
                    'message': 'Cannot leave team as you are the owner'
                },
            }, status=400)
        TeamMember.objects.get(
            user=request.user,
            team=team
        ).delete()
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=200)


class TransferOwnershipView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TransferOwnershipSerializer

    @resolve_team
    @handle_refresh
    def post(self, request, *args, **kwargs):
        data = request.data
        newOwnerID = data.get('userID')
        team = self.team
        if not newOwnerID:
            return Response({
                'error': {
                    'code': "NEW_OWNER_ID_REQUIRED",
                    'message': 'New owner ID is required'
                },
            }, status=400)
        if not team.teammember_set.filter(user=request.user, isOwner=True).exists():
            return Response({
                'error': {
                    'code': "CANNOT_TRANSFER_OWNERSHIP",
                    'message': 'Cannot transfer ownership as you are not the owner'
                },
            }, status=400)
        newOwner = User.objects.get(id=newOwnerID)
        if not team.teammember_set.filter(user=newOwner).exists():
            return Response({
                'error': {
                    'code': "USER_NOT_IN_TEAM",
                    'message': 'User is not in the team'
                },
            }, status=400)
        teamMember = team.teammember_set.get(user=newOwner)
        teamMember.isOwner = True
        teamMember.save()
        teamMember = team.teammember_set.get(user=request.user)
        teamMember.isOwner = False
        teamMember.save()
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=200)


__all__ = [
    'AddTeamMembersView',
    'RemoveTeamMembersView',
    'LeaveTeamView',
    'TransferOwnershipView'
]
