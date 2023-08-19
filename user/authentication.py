from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse


class CookieTokenAuthentication(BaseAuthentication):
    """
    Token-based authentication using cookies.
    """

    def authenticate(self, request):
        access_token = request.COOKIES.get('ACCESS_TOKEN')
        refresh_token = request.COOKIES.get('REFRESH_TOKEN')
        if not access_token:
            return None, None
        authentication = JWTAuthentication()
        try:
            validated_token = authentication.get_validated_token(access_token)
            user = authentication.get_user(validated_token)
            return user, None
        except AuthenticationFailed:
            pass
        if refresh_token:
            try:
                refresh_token = RefreshToken(refresh_token)
                access_token = str(refresh_token.access_token)

                response = JsonResponse({"message": "Token refreshed."})
                response.set_cookie('ACCESS_TOKEN', access_token)
                return None, response
            except Exception:
                pass
        return None, None


__all__ = [
    'CookieTokenAuthentication'
]
