from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from api.views import EndpointsView, VersionsView

urlpatterns = [
    path(
        "",
        VersionsView.as_view(),
        name="versions",
    ),
    path(
        "v2/",
        EndpointsView.as_view(),
        name="endpoints",
    ),
    path("v2/", include("images.urls")),
    path("v2/", include("artists.urls")),
    path("v2/", include("categories.urls")),
    path("v2/", include("characters.urls")),
    path("v2/", include("lists.urls")),
    path("v2/", include("users.urls")),
    path("v2/", include("applications.urls")),
    path("v2/", include("webhooks.urls")),
]
