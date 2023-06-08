from rest_framework.urls import path

from blogs import views

urlpatterns = [
    path("create/", views.BlogListCreateAPIView.as_view(), name="create"),
    path("<int:pk>/list/", views.BlogListRetrieveAPIView.as_view(), name="list"),
    path("<int:pk>/details/", views.BlogRetrieveDetailAPIView.as_view(), name="details"),
    path("<int:pk>/edit/", views.BlogEditRetrieveAPIView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.BlogDeleteAPIView.as_view(), name="delete"),
    path("get-token/", views.ObtainAuthenticationTokenAPIView.as_view(), name="get-token"),
]
