from rest_framework.views import APIView
from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response

from accounts.serializers import UserLoginSerializer


class LoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        user = authenticate(username=username, email=email, password=password)
        if user:
            login(request=request, user=user)
            return Response(data={"msg": "User is logged in successfully!"}, status=200)
        else:
            return Response(data={"msg": "User authentication credentials are failed"}, status=401)


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(data={"msg": "User logged out successfully!"}, status=200)
