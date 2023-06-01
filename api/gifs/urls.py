from django.urls import path

from .views import GifViewSet, GifRelationshipsView


urlpatterns = [
    path("gifs", GifViewSet.as_view({"get": "list"}), name="gif"),
    path(
        "gifs/random",
        GifViewSet.as_view({"get": "retrieve_random"}),
        name="gif-random",
    ),
    path(
        "gifs/random/file",
        GifViewSet.as_view({"get": "retrieve_random_file"}),
        name="gif-random-file",
    ),
    path("gifs/<uuid:pk>", GifViewSet.as_view({"get": "retrieve"}), name="gif-detail"),
    path(
        "gifs/<uuid:pk>/file",
        GifViewSet.as_view({"get": "retrieve_file"}),
        name="gif-file",
    ),
    path(
        r"gifs/<uuid:pk>/verification",
        GifViewSet.as_view({"post": "verification_status"}),
        name="gif-verification",
    ),
    path(
        "gifs/<uuid:pk>/<related_field>",
        GifViewSet.as_view({"get": "retrieve_related"}),
        name="gif-related",
    ),
    path(
        "gifs/<uuid:pk>/relationships/<related_field>",
        GifRelationshipsView.as_view(),
        name="gif-relationships",
    ),
]
