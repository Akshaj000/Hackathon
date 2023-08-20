from rest_framework.response import Response

from user.authentication import CookieTokenAuthentication, set_token_cookies


def handle_refresh(func):
    def wrapper(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        user, tokens = CookieTokenAuthentication().authenticate(request)
        if tokens:
            response = set_token_cookies(response, tokens['ACCESS_TOKEN'], tokens['REFRESH_TOKEN'])
        return response
    return wrapper


def admin_required(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response({
                'error': {
                    'code': 'UNAUTHORIZED',
                    'message': 'You are not authorized to access this resource'
                }
            }, status=401)
        return func(self, request, *args, **kwargs)
    return wrapper


__all__ = [
    'handle_refresh',
    'admin_required'
]


