from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from user.models import User
from user.authentication import CookieTokenAuthentication
from user.serializers import UserSerializer


class ProfileView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


class UpdateProfileView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if data.get("name"):
            user.name = data.get("name")
        if data.get("bio"):
            user.bio = data.get("bio")
        if data.get("avatar"):
            user.avatar = data.get("avatar")
        if data.get("email"):
            if User.objects.filter(email=data.get('email')).exists():
                return Response({
                    'error': {
                        'code': "EMAIL_ALREADY_EXISTS",
                        'message': 'Email already exists'
                    },
                }, status=400)
            user.email = data.get("email")
        if data.get("username"):
            if User.objects.filter(username=data.get('username')).exists():
                return Response({
                    'error': {
                        'code': "USERNAME_ALREADY_EXISTS",
                        'message': 'Username already exists'
                    },
                }, status=400)
            user.username = data.get("username")
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


class DeleteAccountView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        password = request.data.get('password')
        if not user.check_password(password):
            return Response({
                'error': {
                    'code': 'INVALID_PASSWORD',
                    'message': 'Invalid password'
                }
            }, status=400)
        user.delete()
        return Response(status=200)


__all__ = [
    'ProfileView',
    'UpdateProfileView',
    'DeleteAccountView'
]
