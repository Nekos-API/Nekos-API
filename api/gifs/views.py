import secrets

from django.shortcuts import render
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from rest_framework import permissions
from rest_framework_json_api import views, serializers

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
        "categories__name": (
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

        if "token" in request.GET:
            if not re.match(r"^[\w-]{,50}$", request.GET["token"]):
                raise serializers.ValidationError(
                    detail="Token must be up to 50 characters long and URL safe.",
                    code="invalid_shared_resource_token",
                )

            gif_ct = ContentType.objects.get_for_model(Gif)
            shared_resource_token = SharedResourceToken.objects.filter(
                token=request.GET["token"], content_type=gif_ct
            ).first()

            if shared_resource_token is None:
                qs = self.filter_queryset(self.get_queryset())
                gif = qs[secrets.randbelow(len(qs))]

                shared_resource_token = SharedResourceToken.objects.create(
                    token=request.GET["token"],
                    content_type=gif_ct,
                    object_id=gif.id,
                )

            else:
                gif = shared_resource_token.resource

            return Response(GifSerializer(gif, context={"request": request}).data)

        else:
            qs = self.filter_queryset(self.get_queryset())

            return Response(
                GifSerializer(
                    qs[secrets.randbelow(len(qs))], context={"request": request}
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

        if "token" in request.GET:
            if not re.match(r"^[\w-]{,50}$", request.GET["token"]):
                raise serializers.ValidationError(
                    detail="Token must be up to 50 characters long and URL safe.",
                    code="invalid_shared_resource_token",
                )

            gif_ct = ContentType.objects.get_for_model(Gif)
            shared_resource_token = SharedResourceToken.objects.filter(
                token=request.GET["token"], content_type=gif_ct
            ).first()

            if shared_resource_token is None:
                qs = self.filter_queryset(
                    self.get_queryset().exclude(Q(file=None) | Q(file=""))
                )
                gif = qs[secrets.randbelow(len(qs))]

                shared_resource_token = SharedResourceToken.objects.create(
                    token=request.GET["token"],
                    content_type=gif_ct,
                    object_id=gif.id,
                )

            else:
                gif = shared_resource_token.resource

            return HttpResponseRedirect(gif.file.url, status=307)

        else:
            qs = self.filter_queryset(
                self.get_queryset().exclude(Q(file=None) | Q(file=""))
            )
            return HttpResponseRedirect(qs[secrets.randbelow(len(qs))].file.url, status=307)

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
