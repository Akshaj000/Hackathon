from user.authentication import CookieTokenAuthentication, set_token_cookies


def handle_refresh(func):
    def wrapper(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        user, tokens = CookieTokenAuthentication().authenticate(request)
        if tokens:
            response = set_token_cookies(response, tokens['ACCESS_TOKEN'], tokens['REFRESH_TOKEN'])
        return response
    return wrapper


__all__ = [
    'handle_refresh',
]


