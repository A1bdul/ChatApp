from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from user.models import User
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from urllib.parse import parse_qs
from jwt import decode as jwt_decode
from django.conf import settings


@database_sync_to_async
def get_user(validated_token):
    try:
        user = get_user_model().objects.get(id=validated_token)
        return user
    except User.DoesNotExist:
        return AnonymousUser


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        close_old_connections()
        self.inner = inner

    async def __call__(self, scope, receive, send, *args, **kwargs):
        close_old_connections()
        token = parse_qs(scope['query_string'].decode("utf8"))["token"][0]
        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            print(e)
            return None
        else:
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # return decoded jwt token into dictionary
            # {
            #   'token_type': 'access',
            #    'exp': 1666485492,
            #   'jti': 'f44998827fb04307aab3cb675c77e875',
            # ' user_id': 1
            # }
            # print(decoded_data)
            scope['user'] = await get_user(decoded_data['user_id'])
        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))
