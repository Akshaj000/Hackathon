from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.authentication import CookieTokenAuthentication
from user.decorators import handle_refresh, admin_required
from user.models import User
from user.serializers import UserSerializer, UserQueryInputSerializer


class UserView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserQueryInputSerializer

    @handle_refresh
    @admin_required
    def put(self, request):
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
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
