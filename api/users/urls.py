from django.urls import path

from oauth2_provider.views import TokenView, RevokeTokenView

from .views import (
    UserView,
    UserRelationshipsView,
    ExternalAuthAPIViewSet,
    UserAvatarUploadView,
)

urlpatterns = [
    path("users", UserView.as_view({"get": "list"}), name="user"),
    path(
        "users/@me",
        UserView.as_view({"get": "retrieve", "patch": "update"}),
        name="user-me",
        kwargs={"pk": "@me"},
    ),
    path(
        "users/@me/avatar",
        UserAvatarUploadView.as_view(),
        name="user-avatar",
    ),
    path(
        "users/<uuid:pk>",
        UserView.as_view({"get": "retrieve", "patch": "update"}),
        name="user-detail",
    ),
    path(
        "users/<uuid:pk>/follow",
        UserView.as_view({"post": "follow", "delete": "unfollow"}),
        name="user-follow",
    ),
    path(
        "users/<uuid:pk>/<related_field>",
        UserView.as_view({"get": "retrieve_related"}),
        name="user-related",
    ),
    path(
        "users/<uuid:pk>/relationships/<related_field>",
        UserRelationshipsView.as_view(),
        name="user-relationships",
    ),
    path("auth/signup", UserView.as_view({"post": "signup"})),
    path("auth/token", TokenView.as_view(), name="token"),
    path("auth/token/revoke", RevokeTokenView.as_view(), name="revoke-token"),
    path(
        "auth/external/discord",
        ExternalAuthAPIViewSet.as_view({"get": "discord"}),
        name="discord-token",
    ),
]
