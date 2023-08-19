from functools import wraps
from rest_framework.response import Response
from rest_framework import status

from user.models import User
from .models import Team, TeamMember


def resolve_team(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        data = request.data
        team_id = data.get('id')
        if not team_id:
            return Response({
                'error': {
                    'code': "TEAM_ID_REQUIRED",
                    'message': 'Team ID is required'
                },
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            team = Team.objects.get(
                id=team_id
            )
        except Team.DoesNotExist:
            return Response({
                'error': {
                    'code': "TEAM_NOT_FOUND",
                    'message': 'Team not found'
                },
            }, status=status.HTTP_400_BAD_REQUEST)
        if not TeamMember.objects.filter(
            user=request.user,
            team=team
        ).exists():
            return Response({
                'error': {
                    'code': "TEAM_MEMBER_NOT_FOUND",
                    'message': 'Team member not found'
                },
            }, status=status.HTTP_400_BAD_REQUEST)
        self.team = team
        return view_func(self, request, *args, **kwargs)
    return wrapper


def extract_member_ids(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        data = request.data
        members = data.get('members')
        if members is None:
            self.member_ids = []
            return func(self, request, *args, **kwargs)
        if isinstance(members, str):
            member_ids = [int(members)]
        elif isinstance(members, list):
            member_ids = [int(member_id) for member_id in members]
        else:
            return Response({
                'error': {
                    'code': "INVALID_MEMBERS",
                    'message': 'Invalid format for members'
                },
            }, status=400)
        if not User.objects.filter(id__in=member_ids).exists():
            return Response({
                'error': {
                    'code': "USER_NOT_FOUND",
                    'message': 'User not found'
                },
            }, status=400)
        self.member_ids = member_ids
        return func(self, request, *args, **kwargs)

    return wrapper


__all__ = [
    'resolve_team',
    'extract_member_ids',
]
