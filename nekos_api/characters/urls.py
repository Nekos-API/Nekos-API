from django.urls import path

from .views import CharacterViewSet, CharacterRelationshipsView


urlpatterns = [
    path("characters", CharacterViewSet.as_view({"get": "list"}), name="character"),
    path(
        "characters/<uuid:pk>",
        CharacterViewSet.as_view({"get": "retrieve"}),
        name="character-detail",
    ),
    path(
        "characters/<uuid:pk>/follow",
        CharacterViewSet.as_view({"post": "follow", "delete": "unfollow"}),
        name="character-follow",
    ),
    path(
        r"characters/<uuid:pk>/<related_field>",
        CharacterViewSet.as_view({"get": "retrieve_related"}),
        name="character-related",
    ),
    path(
        r"characters/<uuid:pk>/relationships/<related_field>",
        CharacterRelationshipsView.as_view(),
        name="character-relationships",
    ),
]
