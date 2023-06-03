from rest_framework.permissions import BasePermission

import os
from datetime import datetime
from jose import jwt, JWTError


class IsAdminAndHasToken(BasePermission):
    @staticmethod
    def current_unix_seconds():
        current_datetime = datetime.now()
        start_datetime = datetime(1970, 1, 1)

        time_difference = current_datetime - start_datetime
        total_seconds = time_difference.total_seconds()
        return int(total_seconds)

    def has_permission(self, request, view):
        token = request.headers.get("Authorization")
        if (not token) or ("Bearer " not in token):
            return False
        token = token.split()[1]
        # Here 401 status error may occur if os unable to get keys: secret, algorithm
        secret = os.getenv("secret")
        algorithm = os.getenv("algorithm")
        try:
            decoded_token = jwt.decode(token, secret, algorithms=[algorithm])
            if decoded_token.get("exp") < self.current_unix_seconds():
                return False
            return True
        except JWTError:
            return False
