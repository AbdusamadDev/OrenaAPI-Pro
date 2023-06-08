from django.contrib import admin
from blogs.models import CategoryModel, BlogsAPIModel

admin.site.register(CategoryModel)
admin.site.register(BlogsAPIModel)
