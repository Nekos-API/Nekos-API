from django.http import HttpResponse
from django.utils.decorators import method_decorator

from rest_framework import permissions
from rest_framework_json_api import views, serializers

from django_ratelimit.decorators import ratelimit

from utils.decorators import permission_classes

from .models import Artist
from .serializers import ArtistSerializer

# Create your views here.


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


class ArtistRelationshipsView(views.RelationshipView):
    queryset = Artist.objects.all()

    def get_permissions(self):
        if self.request.method != "GET":
            return [permissions.IsAdminUser]
        return []
