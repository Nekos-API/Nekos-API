from django.urls import path

from .views import CategoryViewSet, CategoryRelationshipsView


urlpatterns = [
    path("categories", CategoryViewSet.as_view({"get": "list"}), name="category"),
    path(
        "categories/<uuid:pk>",
        CategoryViewSet.as_view({"get": "retrieve"}),
        name="category-detail",
    ),
    path(
        "categories/<uuid:pk>/follow",
        CategoryViewSet.as_view({"post": "follow", "delete": "unfollow"}),
        name="category-follow",
    ),
    path(
        r"categories/<uuid:pk>/<related_field>",
        CategoryViewSet.as_view({"get": "retrieve_related"}),
        name="category-related",
    ),
    path(
        r"categories/<uuid:pk>/relationships/<related_field>",
        CategoryRelationshipsView.as_view(),
        name="category-relationships",
    ),
]
