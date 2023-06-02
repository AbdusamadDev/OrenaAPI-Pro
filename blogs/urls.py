from rest_framework.urls import path

from blogs import views

urlpatterns = [
    path("create/", views.BlogListCreateAPIView.as_view(), name="create"),
]
