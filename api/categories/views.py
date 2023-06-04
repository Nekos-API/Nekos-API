from django.http import HttpResponse
from django.utils.decorators import method_decorator

from rest_framework import permissions
from rest_framework_json_api import views, serializers

from django_ratelimit.decorators import ratelimit

from utils.decorators import permission_classes

from .models import Category
from .serializers import CategorySerializer

# Create your views here.


class CategoryViewSet(views.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
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

    prefetch_for_includes = {"followers": ["followers"], "images": ["images"]}


class CategoryRelationshipsView(views.RelationshipView):
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.request.method != "GET":
            return [permissions.IsAdminUser]
        return []
