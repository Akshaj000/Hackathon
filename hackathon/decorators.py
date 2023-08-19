from functools import wraps
from rest_framework.response import Response

from user.models import User


def extract_organiser_ids(func):
    
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        data = request.data
        organisers = data.get('organisers')
        if organisers is None:
            self.organiser_ids = []
            return func(self, request, *args, **kwargs)
        if isinstance(organisers, str):
            organiser_ids = [int(organisers)]
        elif isinstance(organisers, list):
            organiser_ids = [int(member_id) for member_id in organisers]
        else:
            return Response({
                'error': {
                    'code': "INVALID_MEMBERS",
                    'message': 'Invalid format for members'
                },
            }, status=400)
        if not User.objects.filter(id__in=organiser_ids).exists():
            return Response({
                'error': {
                    'code': "USER_NOT_FOUND",
                    'message': 'User not found'
                },
            }, status=400)
        self.organiser_ids = organiser_ids
        return func(self, request, *args, **kwargs)

    return wrapper


__all__ = [
    'extract_organiser_ids',
]

