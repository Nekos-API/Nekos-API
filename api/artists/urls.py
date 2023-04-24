from django.urls import path

from .views import ArtistViewSet, ArtistRelationshipsView


urlpatterns = [
    path("artists", ArtistViewSet.as_view({"get": "list"}), name="artist"),
    path(
        "artists/<uuid:pk>",
        ArtistViewSet.as_view({"get": "retrieve"}),
        name="artist-detail",
    ),
    path(
        "artists/<uuid:pk>/follow",
        ArtistViewSet.as_view({"post": "follow", "delete": "unfollow"}),
        name="artist-follow",
    ),
    path(
        r"artists/<uuid:pk>/<related_field>",
        ArtistViewSet.as_view({"get": "retrieve_related"}),
        name="artist-related",
    ),
    path(
        r"artists/<uuid:pk>/relationships/<related_field>",
        ArtistRelationshipsView.as_view(),
        name="artist-relationships",
    ),
]
