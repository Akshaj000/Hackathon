from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from user.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from datetime import datetime, timedelta

from user.serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from user.authentication import CookieTokenAuthentication


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Get the token data from the response
        token_data = response.data
        # Set the access token as a cookie
        access_token = token_data['access']
        response.set_cookie(
            key='ACCESS_TOKEN',
            value=access_token,
            # Set the expiration time for the cookie (1 hour for access token)
            expires=datetime.now() + timedelta(hours=1),
            # Set same site attribute to 'Lax' to prevent cross-site request forgery (CSRF) attacks
            samesite='Lax'
        )
        # Set the refresh token as a cookie
        refresh_token = token_data['refresh']
        response.set_cookie(
            key='REFRESH_TOKEN',
            value=refresh_token,
            # Set the expiration time for the cookie (30 days for refresh token)
            expires=datetime.now() + timedelta(days=30),
            samesite='Lax',
        )
        return response


class UserRegisterView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        # Check if user is already logged with cookies
        if request.COOKIES.get('access') or request.user.is_authenticated:
            return Response({
                'error': {
                    'code': "ALREADY_LOGGED_IN",
                    'message': 'You are already logged in'
                },
            }, status=400)

        # get the data from the request
        data = request.data
        for field in ['email', 'name', 'username', 'password']:
            if not data.get(field):
                return Response({
                    'error': {
                        'code': "MISSING_FIELD",
                        'message': f'{field} is required'
                    },
                }, status=400)

        # Check if user already exists
        if User.objects.filter(email=data.get('email')).exists():
            return Response({
                'error': {
                    'code': "EMAIL_ALREADY_EXISTS",
                    'message': 'Email already exists'
                },
            }, status=400)

        # Create the user
        user = User.objects.create_user(
            email=data.get('email'),
            name=data.get('name'),
            username=data.get('username')
        )
        user.set_password(data.get('password'))
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


class UserLogoutView(APIView):
    # Set the authentication and permission classes
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Delete the access and refresh token cookies
        response = Response(status=200)
        response.delete_cookie('ACCESS_TOKEN')
        response.delete_cookie('REFRESH_TOKEN')
        return response


__all__ = [
    'UserRegisterView',
    'UserLoginView',
    'UserLogoutView',
]
