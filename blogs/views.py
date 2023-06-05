from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_201_CREATED
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView
)

from blogs.permissions import IsAdminAndHasToken
from blogs.models import BlogsAPIModel
from blogs.pagination import BlogPagination
from blogs.serializers import BlogsAPISerializer, JWTTokenSerializer


def home(request):
    return render(request, "home.html", {})


class BlogListCreateAPIView(CreateAPIView):
    model = BlogsAPIModel
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminAndHasToken]
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


class BlogRetrieveDetailAPIView(RetrieveAPIView):
    model = BlogsAPIModel
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


class BlogEditRetrieveAPIView(RetrieveUpdateAPIView):
    model = BlogsAPIModel
    serializer_class = BlogsAPISerializer
    queryset = BlogsAPIModel.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminAndHasToken]


class BlogDeleteAPIView(DestroyAPIView):
    model = BlogsAPIModel
    queryset = BlogsAPIModel.objects.all()
    serializer_class = BlogsAPISerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminAndHasToken]


class JWTObtainTokenView(ObtainAuthToken):
    serializer_class = JWTTokenSerializer
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return Response({'token': token['token']})
