from user.models import User

from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from .models import Hackathon, Organiser


def resolve_hackathon(action):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            data = request.data
            hackathon_id = data.get('id')
            if not hackathon_id:
                return Response({
                    'error': {
                        'code': "HACKATHON_ID_REQUIRED",
                        'message': 'Hackathon ID is required'
                    },
                }, status=status.HTTP_400_BAD_REQUEST)
            print(hackathon_id)
            try:
                hackathon = Hackathon.objects.get(id=hackathon_id)
            except Hackathon.DoesNotExist:
                return Response({
                    'error': {
                        'code': "HACKATHON_NOT_FOUND",
                        'message': 'Hackathon not found'
                    },
                }, status=status.HTTP_404_NOT_FOUND)
            if request.user.is_admin:
                self.hackathon = hackathon
                return view_func(self, request, *args, **kwargs)
            # Apply different access checks based on the action
            if action == "admin":
                allowed_access_levels = [0]
            elif action == "editor":
                allowed_access_levels = [0, 1]
            else:
                allowed_access_levels = [0, 1, 2]
            if not Organiser.objects.filter(
                user=request.user,
                hackathon=hackathon,
                access__in=allowed_access_levels
            ).exists():
                return Response({
                    'error': {
                        'code': "ACCESS_DENIED",
                        'message': 'Access denied'
                    },
                }, status=status.HTTP_401_UNAUTHORIZED)
            self.hackathon = hackathon
            return view_func(self, request, *args, **kwargs)
        return wrapper
    return decorator


__all__ = [
    'resolve_hackathon'
]
