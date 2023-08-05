from django.http import HttpResponse
from django.utils.decorators import method_decorator

from rest_framework import permissions

from rest_framework_json_api import views, serializers

from django_ratelimit.decorators import ratelimit

from utils.decorators import permission_classes

from characters.models import Character
from characters.serializers import CharacterSerializer

# Create your views here.


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
            "in",
        ),
        "last_name": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "in",
        ),
        "description": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "in",
        ),
        "gender": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "in",
        ),
        "species": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "in",
        ),
        "nationality": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "in",
        ),
        "created_at": ("exact", "second", "minute", "hour", "day", "month", "year"),
        "updated_at": ("exact", "second", "minute", "hour", "day", "month", "year"),
    }


class CharacterRelationshipsView(views.RelationshipView):
    queryset = Character.objects.all()

    def get_permissions(self):
        if self.request.method != "GET":
            return [permissions.IsAdminUser]
        return []
