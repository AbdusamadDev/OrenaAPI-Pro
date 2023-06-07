from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime, timedelta, timezone


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except ObjectDoesNotExist:
            raise AuthenticationFailed("Invalid Token.")

        date_token = token.created + timedelta(days=30)
        if date_token < datetime.now(timezone.utc):
            raise AuthenticationFailed("Token Expired.")

        return (token.user, token)
