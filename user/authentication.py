from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookieTokenAuthentication(BaseAuthentication):
    """
    Token-based authentication using cookies.
    """

    def authenticate(self, request):
        access_token = request.COOKIES.get('ACCESS_TOKEN')
        if not access_token:
            return None

        authentication = JWTAuthentication()
        try:
            validated_token = authentication.get_validated_token(access_token)
            user = authentication.get_user(validated_token)
        except AuthenticationFailed:
            return None, None
        return user, None


__all__ = [
    'CookieTokenAuthentication'
]
