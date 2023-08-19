from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from user.serializers import UserRegistrationSerializer, UserLoginSerializer
from user.authentication import CookieTokenAuthentication, set_token_cookies


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token_data = response.data
        access_token = token_data['access']
        refresh_token = token_data['refresh']
        response = Response(status=200)
        set_token_cookies(response, access_token, refresh_token)
        return response


class UserRegisterView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        for field in ['email', 'name', 'username', 'password']:
            if not data.get(field):
                return Response({
                    'error': {
                        'code': "MISSING_FIELD",
                        'message': f'{field} is required'
                    },
                }, status=400)
        if User.objects.filter(email=data.get('email')).exists():
            return Response({
                'error': {
                    'code': "EMAIL_ALREADY_EXISTS",
                    'message': 'Email already exists'
                },
            }, status=400)
        user = User.objects.create_user(
            email=data.get('email'),
            name=data.get('name'),
            username=data.get('username')
        )
        user.set_password(data.get('password'))
        user.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        response = Response(status=200)
        set_token_cookies(response, access_token, refresh.token)
        return response


class UserLogoutView(APIView):
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = Response(status=200)
        response.delete_cookie('ACCESS_TOKEN')
        response.delete_cookie('REFRESH_TOKEN')
        return response


__all__ = [
    'UserRegisterView',
    'UserLoginView',
    'UserLogoutView',
]
