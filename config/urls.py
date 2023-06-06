from django.contrib import admin
from django.urls import path, include

from blogs.views import home

urlpatterns = [
    path("", home, name="home"),
    path('admin/', admin.site.urls),
    path("blogs/", include("blogs.urls")),
]
