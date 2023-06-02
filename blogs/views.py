from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK
)

from blogs.models import BlogsAPIModel
from blogs.serializers import BlogsAPISerializer


class BlogListCreateAPIView(ListCreateAPIView):
    model = BlogsAPIModel
    queryset = BlogsAPIModel.objects.all()
    serializer_class = BlogsAPISerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print({"data": queryset})
        # assert queryset is None, ObjectDoesNotExist("Database is empty.")
        paginated_query = self.pagination_class().paginate_queryset(queryset=queryset, request=request, view=self)
        serializer = self.get_serializer(paginated_query, many=True)
        data = self.pagination_class().get_paginated_response(data=serializer.data)
        return data

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get("title")
            content = serializer.validated_data.get("content")
            image = serializer.validated_data.get("image")

            record = self.model(
                title=title,
                content=content,
                image=image
            )
            record.save()
            success_list = self.list(request, *args, **kwargs)
            return Response(data=success_list, status=HTTP_201_CREATED)
        else:
            raise ValidationError("Serializer validation failed!")

# Paginationda muammosi qoldi. tugirlash kerak
