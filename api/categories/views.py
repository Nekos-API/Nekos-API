from django.http import HttpResponse
from django.utils.decorators import method_decorator

from rest_framework import permissions
from rest_framework_json_api import views, serializers

from django_ratelimit.decorators import ratelimit

from utils.decorators import permission_classes

from .models import Category
from .serializers import CategorySerializer

# Create your views here.


@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="list")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="retrieve")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="retrieve_related")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="follow")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="unfollow")
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
        "created_at": ("second", "minute", "hour", "day", "month", "year"),
        "updated_at": ("second", "minute", "hour", "day", "month", "year"),
    }

    prefetch_for_includes = {"followers": ["followers"], "images": ["images"]}

    @permission_classes([permissions.IsAuthenticated])
    def follow(self, request, *args, **kwargs):
        """
        Follow the artist.
        """

        category = self.get_object()

        if category.followers.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                {
                    "id": "category_already_followed",
                    "detail": "You are already following this category.",
                    "source": {
                        "pointer": "/data",
                    },
                }
            )

        request.user.followed_categories.add(category)

        return HttpResponse("", status=204)

    @permission_classes([permissions.IsAuthenticated])
    def unfollow(self, request, *args, **kwargs):
        """
        Follow the artist.
        """

        category = self.get_object()

        if not category.followers.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                {
                    "id": "category_not_followed",
                    "detail": "You are not following this category.",
                    "source": {
                        "pointer": "/data",
                    },
                }
            )

        request.user.followed_categories.remove(category)

        return HttpResponse("", status=204)


@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="get")
class CategoryRelationshipsView(views.RelationshipView):
    queryset = Category.objects.all()
