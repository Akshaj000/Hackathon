from rest_framework.response import Response
from rest_framework.views import APIView

from user.decorators import handle_refresh, admin_required
from user.models import User
from user.serializers import UserSerializer


class UserView(APIView):

    @handle_refresh
    @admin_required
    def get(self, request):
        data = request.data
        try:
            user = User.objects.get(id=data.get('id'))
        except User.DoesNotExist:
            return Response({
                'error': {
                    'code': 'USER_NOT_FOUND',
                    'message': 'User not found'
                }
            }, status=404)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


class UsersView(APIView):

    @handle_refresh
    @admin_required
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=200)


__all__ = [
    'UserView',
    'UsersView'
]
