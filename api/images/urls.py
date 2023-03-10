from django.urls import path

from .views import ImagesViewSet, ImageRelationshipsView

urlpatterns = [
    path("images", ImagesViewSet.as_view({"get": "list", "post": "create"}), name="image"),
    path("images/random", ImagesViewSet.as_view({"get": "retrieve_random"}), name="image-random"),
    path("images/random/file", ImagesViewSet.as_view({"get": "retrieve_random_file"}), name="image-random-file"),
    path(
        "images/<uuid:pk>",
        ImagesViewSet.as_view({"get": "retrieve", "patch": "update", "delete": "delete"}),
        name="image-detail",
    ),
    path(
        "images/<uuid:pk>/file",
        ImagesViewSet.as_view({"get": "retrieve_file"}),
        name="image-file",
    ),
    path(
        r"images/<uuid:pk>/like",
        ImagesViewSet.as_view({"post": "like", "delete": "unlike"}),
        name="image-like",
    ),
    path(
        r"images/<uuid:pk>/save",
        ImagesViewSet.as_view({"post": "save", "delete": "unsave"}),
        name="image-save",
    ),
    path(
        r"images/<uuid:pk>/verification",
        ImagesViewSet.as_view({"post": "verification_status"}),
        name="image-verification",
    ),
    path(
        r"images/<uuid:pk>/<related_field>",
        ImagesViewSet.as_view({"get": "retrieve_related"}),
        name="image-related",
    ),
    path(
        r"images/<uuid:pk>/relationships/<related_field>",
        ImageRelationshipsView.as_view(),
        name="image-relationships",
    ),
]
