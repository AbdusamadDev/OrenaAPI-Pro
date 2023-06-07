# from rest_framework.permissions import BasePermission
# from rest_framework.authtoken.models import Token
#
# from datetime import datetime, timezone, timedelta
#
#
# class TokenPermission(BasePermission):
#     def has_permission(self, request, view):
#         token = request.headers.get("Authorization")
#         if "Token " not in token:
#             return False
#         token = token.split()[-1]
#         object_token = Token.objects.get(pk=token)
#         if not object_token:
#             return False
#
#         date_token = object_token.created + timedelta(days=30)
#         if date_token < datetime.now(timezone.utc):
#             return False