from django.http import HttpResponse
from django.utils.decorators import method_decorator

from rest_framework import permissions
from rest_framework_json_api import views, serializers

from django_ratelimit.decorators import ratelimit

from utils.decorators import permission_classes

from .models import Artist
from .serializers import ArtistSerializer

# Create your views here.


@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="list")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="retrieve")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="retrieve_related")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="follow")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="unfollow")
class ArtistViewSet(views.ModelViewSet):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()
    prefetch_for_includes = {"followers": ["followers"], "images": ["images"]}
    ordering_fields = [
        "name",
        "created_at",
        "updated_at",
    ]
    filterset_fields = {
        "name": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "in",
            "startswith",
            "endswith",
            "regex",
            "iregex",
        ),
        "created_at": ("exact", "second", "minute", "hour", "day", "month", "year"),
        "updated_at": ("exact", "second", "minute", "hour", "day", "month", "year"),
    }

    @permission_classes([permissions.IsAuthenticated])
    def follow(self, request, *args, **kwargs):
        """
        Follow the artist.
        """

        artist = self.get_object()

        if artist.followers.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                {
                    "id": "artist_already_followed",
                    "detail": "You are already following this artist.",
                    "source": {
                        "pointer": "/data",
                    },
                }
            )

        request.user.followed_artists.add(artist)

        return HttpResponse("", status=204)

    @permission_classes([permissions.IsAuthenticated])
    def unfollow(self, request, *args, **kwargs):
        """
        Follow the artist.
        """

        artist = self.get_object()

        if not artist.followers.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                {
                    "id": "artist_not_followed",
                    "detail": "You are not following this artist.",
                    "source": {
                        "pointer": "/data",
                    },
                }
            )

        request.user.followed_artists.remove(artist)

        return HttpResponse("", status=204)


@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="get")
class ArtistRelationshipsView(views.RelationshipView):
    queryset = Artist.objects.all()
