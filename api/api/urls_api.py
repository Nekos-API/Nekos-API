from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from api.views_api import EndpointsView

urlpatterns = [
    path("v2" + ("/" if settings.DEBUG else ""), EndpointsView.as_view(), name="endpoints"),
    path("v2" + ("/" if settings.DEBUG else ""), include("images.urls")),
    path("v2" + ("/" if settings.DEBUG else ""), include("artists.urls")),
    path("v2" + ("/" if settings.DEBUG else ""), include("categories.urls")),
    path("v2" + ("/" if settings.DEBUG else ""), include("characters.urls")),
    path("v2" + ("/" if settings.DEBUG else ""), include("users.urls")),
    path("v2" + ("/" if settings.DEBUG else ""), include("lists.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)