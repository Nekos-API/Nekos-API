from django.http import HttpResponse
from django.utils.decorators import method_decorator

from rest_framework import permissions

from rest_framework_json_api import views, serializers

from django_ratelimit.decorators import ratelimit

from utils.decorators import permission_classes

from .models import Character
from .serializers import CharacterSerializer

# Create your views here.


@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="list")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="retrieve")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="retrieve_related")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="follow")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="unfollow")
class CharacterViewSet(views.ReadOnlyModelViewSet):
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()
    prefetch_for_includes = {
        "images": ["images"],
        "followers": ["followers"],
    }
    ordering_fields = [
        "first_name",
        "last_name",
        "description",
        "gender",
        "species",
        "ages",
        "birth_date",
        "nationality",
        "occupations",
        "created_at",
        "updated_at",
    ]
    filterset_fields = {
        "first_name": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "regex",
            "in",
            "iregex",
        ),
        "last_name": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "regex",
            "in",
            "iregex",
        ),
        "description": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "regex",
            "in",
            "iregex",
        ),
        "gender": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "regex",
            "in",
            "iregex",
        ),
        "species": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "regex",
            "in",
            "iregex",
        ),
        "nationality": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "regex",
            "in",
            "iregex",
        ),
        "occupations": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "regex",
            "in",
            "iregex",
        ),
        "created_at": ("second", "minute", "hour", "day", "month", "year"),
        "updated_at": ("second", "minute", "hour", "day", "month", "year"),
    }

    @permission_classes([permissions.IsAuthenticated])
    def follow(self, request, *args, **kwargs):
        """
        Follow the artist.
        """

        character = self.get_object()

        if character.followers.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                {
                    "id": "character_already_followed",
                    "detail": "You are already following this character.",
                    "source": {
                        "pointer": "/data",
                    },
                }
            )

        request.user.followed_characters.add(character)

        return HttpResponse("", status=204)

    @permission_classes([permissions.IsAuthenticated])
    def unfollow(self, request, *args, **kwargs):
        """
        Follow the artist.
        """

        character = self.get_object()

        if not character.followers.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                {
                    "id": "character_not_followed",
                    "detail": "You are not following this character.",
                    "source": {
                        "pointer": "/data",
                    },
                }
            )

        request.user.followed_characters.remove(character)

        return HttpResponse("", status=204)


@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="get")
class CharacterRelationshipsView(views.RelationshipView):
    queryset = Character.objects.all()
