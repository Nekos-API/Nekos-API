from django.urls import path

from .views import LoginView, ExternalAuthAPIViewSet


urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path(
        "external/discord",
        ExternalAuthAPIViewSet.as_view({"get": "go_to_oauth"}),
        kwargs={"provider": "discord"},
    ),
    path(
        "external/google",
        ExternalAuthAPIViewSet.as_view({"get": "go_to_oauth"}),
        kwargs={"provider": "google"},
    ),
    path(
        "external/github",
        ExternalAuthAPIViewSet.as_view({"get": "go_to_oauth"}),
        kwargs={"provider": "github"},
    ),
    path(
        "external/discord/callback",
        ExternalAuthAPIViewSet.as_view({"get": "discord"}),
    ),
    path(
        "external/google/callback",
        ExternalAuthAPIViewSet.as_view({"get": "google"}),
    ),
    path(
        "external/github/callback",
        ExternalAuthAPIViewSet.as_view({"get": "github"}),
    ),
]
