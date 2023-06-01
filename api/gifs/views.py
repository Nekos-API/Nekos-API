from django.shortcuts import render

from rest_framework import permissions
from rest_framework_json_api import views

from utils.decorators import permission_classes

from .models import Gif
from .serializers import GifSerializer

# Create your views here.


class GifViewSet(views.ModelViewSet):
    serializer_class = GifSerializer

    filterset_fields = {
        "reactions__name": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "regex",
            "iregex",
        ),
        "is_spoiler": ("exact",),
        "age_rating": ("exact", "iexact", "in", "isnull", "regex", "iregex"),
        "height": ("exact", "lt", "lte", "gt", "gte"),
        "width": ("exact", "lt", "lte", "gt", "gte"),
        "aspect_ratio": ("exact", "startswith", "endswith", "regex"),
        "orientation": ("iexact", "isnull"),
        "verification_status": (
            "exact",
            "iexact",
            "in",
            "contains",
            "icontains",
            "regex",
            "iregex",
        ),
        "source_name": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "isnull",
            "regex",
            "iregex",
        ),
        "source_url": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "isnull",
            "regex",
            "iregex",
        ),
    }
    select_for_includes = {
        "uploader": ["uploader"],
    }
    prefetch_for_includes = {
        "categories": ["categories"],
        "characters": ["characters"],
        "reactions": ["reactions"],
    }
    ordering_fields = [
        "created_at",
        "updated_at",
        "height",
        "width",
        "age_rating",
        "is_spoiler",
        "verification_status",
        "frames",
        "duration",
        "file_size",
    ]

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Gif.objects.all()
        return Gif.objects.filter(verification_status=Gif.VerificationStatus.VERIFIED)

    def retrieve_random(self, request, *args, **kwargs):
        """
        Returns a random gif object.
        """

        qs = self.filter_queryset(self.get_queryset())

        return Response(
            GifSerializer(
                qs[secrets.randbelow(qs.count())], context={"request": request}
            ).data
        )

    def retrieve_file(self, request, *args, **kwargs):
        """
        Returns a redirect to the selected gif's gif URL.
        """

        pk = kwargs.get("pk")

        gif = get_object_or_404(Gif, pk=pk)

        if not gif.file:
            # Failed Dependency. There is no file for that gif
            return HttpResponse("", status=424)

        return HttpResponseRedirect(gif.file.url, status=307)

    def retrieve_random_file(self, request, *args, **kwargs):
        """
        Returns a redirect to a random gif's gif URL.
        """

        qs = self.filter_queryset(self.get_queryset().exclude(file=None))

        gif = qs[secrets.randbelow(qs.count())]

        return HttpResponseRedirect(gif.file.url, status=307)

    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    def verification_status(self, request, pk):
        """
        Verify a gif.
        """

        gif = get_object_or_404(Gif, pk=pk)
        gif.verification_status = Gif.VerificationStatus(request.GET.get("status"))
        gif.save()

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(Gif).pk,
            object_id=gif.id,
            object_repr=gif.title,
            action_flag=CHANGE,
        )

        return Response(GifSerializer(gif, context={"request": request}).data)


class GifRelationshipsView(views.RelationshipView):
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Gif.objects.all()
        return Gif.objects.filter(verification_status=Gif.VerificationStatus.VERIFIED)

    def get_permissions(self):
        if self.request.method != "GET":
            return [permissions.IsAdminUser]
        return []
