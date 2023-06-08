from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import authenticate
from django.shortcuts import render
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView
)

from blogs.models import BlogsAPIModel
from blogs.pagination import BlogPagination
from blogs.serializers import BlogsAPISerializer, UserAuthSerializer


def home(request):
    return render(request, "home.html", {})


class BlogListCreateAPIView(CreateAPIView):
    model = BlogsAPIModel
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = BlogsAPIModel.objects.all()
    serializer_class = BlogsAPISerializer

    def get(self, request, pk, *args, **kwargs):
        blog = self.model.objects.get(pk=pk)

        # Check if the blog has been viewed in the current session
        if not request.session.get(f'blog_viewed_{blog.pk}'):
            blog.view_count += 1
            blog.save()
            request.session[f'blog_viewed_{blog.pk}'] = True
        return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
        else:
            raise ValidationError("Serializer validation failed!")

    def perform_create(self, serializer):
        serializer.save()


class BlogListRetrieveAPIView(ListAPIView):
    model = BlogsAPIModel
    queryset = BlogsAPIModel.objects.all()
    pagination_class = BlogPagination
    serializer_class = BlogsAPISerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        queryset = self.queryset.filter(category_id=self.kwargs.get("pk"))
        return queryset


class BlogRetrieveDetailAPIView(RetrieveAPIView):
    model = BlogsAPIModel
    queryset = BlogsAPIModel.objects.all()
    serializer_class = BlogsAPISerializer

    def get(self, request, pk, *args, **kwargs):
        try:
            blog = self.model.objects.get(pk=pk)
            # Check if the blog has been viewed in the current session
            if not request.session.get(f'blog_viewed_{blog.pk}'):
                blog.view_count += 1
                blog.save()
                request.session[f'blog_viewed_{blog.pk}'] = True
            return super().get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response(
                data={"msg": "Data you are searching does not exist!"},
                status=HTTP_404_NOT_FOUND
            )


class BlogEditRetrieveAPIView(RetrieveUpdateAPIView):
    model = BlogsAPIModel
    serializer_class = BlogsAPISerializer
    queryset = BlogsAPIModel.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            super().get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response(
                data={"msg": "Data you are searching does not exist!"},
                status=HTTP_404_NOT_FOUND
            )


class BlogDeleteAPIView(DestroyAPIView):
    model = BlogsAPIModel
    queryset = BlogsAPIModel.objects.all()
    serializer_class = BlogsAPISerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ObtainAuthenticationTokenAPIView(ObtainAuthToken):
    serializer_class = UserAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data.get("username"),
            password=serializer.validated_data.get("password")
        )
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={"msg": str(token)}, status=HTTP_201_CREATED)
        return Response(data={"msg": "Authentication credentials failed!"}, status=HTTP_401_UNAUTHORIZED)
