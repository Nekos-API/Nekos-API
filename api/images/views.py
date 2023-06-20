import re

import secrets

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.db.models import Q
from django.core.files import File
from django.utils.decorators import method_decorator
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.clickjacking import xframe_options_exempt

from rest_framework import permissions, parsers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_json_api import views, serializers

from django_ratelimit.decorators import ratelimit

from api.models import SharedResourceToken

from utils.decorators import permission_classes

from .models import Image
from .serializers import ImageSerializer


class ImagesViewSet(views.ModelViewSet):
    serializer_class = ImageSerializer
    filterset_fields = {
        "id": ("exact", "in", "regex", "iregex"),
        "title": (
            "exact",
            "iexact",
            "contains",
            "icontains",
            "startswith",
            "endswith",
            "regex",
            "iregex",
        ),
        "age_rating": ("exact", "iexact", "in", "isnull", "regex", "iregex"),
        "height": ("exact", "lt", "lte", "gt", "gte"),
        "width": ("exact", "lt", "lte", "gt", "gte"),
        "aspect_ratio": ("exact", "startswith", "endswith", "regex"),
        "orientation": ("exact", "iexact", "isnull"),
        "is_original": ("exact", "isnull"),
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
        "artist__name": (
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
        "categories__name": (
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
        "characters__first_name": (
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
        "characters__last_name": (
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
        "characters__gender": (
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
        "characters__species": (
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
        "characters__nationality": (
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
        "__all__": ["artist"],
        "uploader": ["uploader"],
    }
    prefetch_for_includes = {
        "categories": ["categories"],
        "characters": ["characters"],
        "liked_by": ["liked_by"],
    }
    ordering_fields = [
        "created_at",
        "updated_at",
        "height",
        "width",
        "age_rating",
        "title",
        "is_original",
        "verification_status",
    ]
    search_fields = [
        "title",
        "categories__name",
        "artist__name",
        "characters__first_name",
        "characters__last_name",
    ]

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Image.objects.all()
        return Image.objects.filter(
            verification_status=Image.VerificationStatus.VERIFIED
        )

    def retrieve_random(self, request, *args, **kwargs):
        """
        Returns a random image object.
        """

        if "token" in request.GET:
            if not re.match(r"^[\w-]{,50}$", request.GET["token"]):
                raise serializers.ValidationError(
                    detail="Token must be up to 50 characters long and URL safe.",
                    code="invalid_shared_resource_token",
                )

            image_ct = ContentType.objects.get_for_model(Image)
            shared_resource_token = SharedResourceToken.objects.filter(
                token=request.GET["token"], content_type=image_ct
            ).first()

            if shared_resource_token is None:
                qs = self.filter_queryset(self.get_queryset())
                image = qs[secrets.randbelow(len(qs))]

                shared_resource_token = SharedResourceToken.objects.create(
                    token=request.GET["token"],
                    content_type=image_ct,
                    object_id=image.id,
                )

            else:
                image = shared_resource_token.resource

            return Response(ImageSerializer(image, context={"request": request}).data)

        else:
            qs = self.filter_queryset(self.get_queryset())

            return Response(
                ImageSerializer(
                    qs[secrets.randbelow(len(qs))], context={"request": request}
                ).data
            )

    def retrieve_file(self, request, *args, **kwargs):
        """
        Returns a redirect to the selected image's image URL.
        """

        pk = kwargs.get("pk")

        image = get_object_or_404(Image, pk=pk)

        if not image.file:
            # Failed Dependency. There is no file for that image
            return HttpResponse("", status=424)

        return HttpResponseRedirect(image.file.url, status=307)

    def retrieve_random_file(self, request, *args, **kwargs):
        """
        Returns a redirect to a random image's image URL.
        """

        if "token" in request.GET:
            if not re.match(r"^[\w-]{,50}$", request.GET["token"]):
                raise serializers.ValidationError(
                    detail="Token must be up to 50 characters long and URL safe.",
                    code="invalid_shared_resource_token",
                )

            image_ct = ContentType.objects.get_for_model(Image)
            shared_resource_token = SharedResourceToken.objects.filter(
                token=request.GET["token"], content_type=image_ct
            ).first()

            if shared_resource_token is None:
                qs = self.filter_queryset(
                    self.get_queryset().exclude(Q(file=None) | Q(file=""))
                )
                image = qs[secrets.randbelow(len(qs))]

                shared_resource_token = SharedResourceToken.objects.create(
                    token=request.GET["token"],
                    content_type=image_ct,
                    object_id=image.id,
                )

            else:
                image = shared_resource_token.resource

            return HttpResponseRedirect(image.file.url, status=307)

        else:
            qs = self.filter_queryset(
                self.get_queryset().exclude(Q(file=None) | Q(file=""))
            )
            return HttpResponseRedirect(qs[secrets.randbelow(len(qs))].file.url, status=307)

    @permission_classes([permissions.IsAuthenticated])
    def create(self, request, *args, **kwargs):
        """
        Creates a new unverified image.
        """

        if request.user.uploaded_images.filter(file=None).count() >= 3:
            raise serializers.ValidationError(
                detail="You have more than 3 images created without a file uploaded. Upload those files (https://api.nekosapi.com/v2/images/:id/file) or delete the images before creating a new one.",
                code="missing_file_uploads",
            )

        return super().create(request, *args, **kwargs)

    @permission_classes([permissions.IsAuthenticated])
    def update(self, request, *args, **kwargs):
        """
        Updates an existent image.
        """

        image = get_object_or_404(
            self.get_queryset().select_related("uploader"), pk=kwargs.get("pk")
        )

        if not request.user.is_staff:
            if request.user != image.uploader:
                raise serializers.ValidationError(
                    detail="You cannot update an image that you have not originally posted.",
                    code="cannot_update_unowned_image",
                )

        return super().update(request, *args, **kwargs)

    @permission_classes([permissions.IsAuthenticated])
    def delete(self, request, pk):
        """
        Delete an image.
        """

        image = get_object_or_404(self.get_queryset().select_related("uploader"), pk=pk)

        if not request.user.is_superuser:
            if request.user != image.uploader:
                raise serializers.ValidationError(
                    detail="You cannot delete an image that you have not originally posted.",
                    code="cannot_delete_unowned_image",
                )

        image.delete()

        return Response(data="", status=204)

    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    def verification_status(self, request, pk):
        """
        Verify an image.
        """

        image = get_object_or_404(Image, pk=pk)
        image.verification_status = Image.VerificationStatus(request.GET.get("status"))
        image.save()

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(Image).pk,
            object_id=image.id,
            object_repr=image.title,
            action_flag=CHANGE,
        )

        return Response(ImageSerializer(image, context={"request": request}).data)


class UploadImageFileView(APIView):
    """
    This view handles the image file upload.
    """

    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> Image:
        """
        Returns the Image object specified by the `pk` path parameter. This
        view is restricted to file uploaders and to moderators, so other
        requests are declined with a 403 Forbidden error.
        """
        image = self.get_queryset().get(pk=int(self.kwargs.get("pk")))

        if image.user != self.request.user and not self.request.user.is_superuser:
            raise serializers.ValidationError(
                detail="You don't have permission to edit this image.",
                code="forbidden",
            )

        return image

    def put(self, request, pk):
        """
        This method handles the file upload. Image files must not be bigger
        than 8 MB. The image can only be modified when it has not been reviewed
        by an administrator (when the verification status is `not_reviewed`).
        Once that it has been reviewed by a moderator, it cannot be modified
        since that would require a re-verification.
        """

        instance = self.get_object()

        file_bytes = request.data["file"].file

        # Prevent from uploading files > 8 MB size
        if file_bytes.getbuffer().nbytes > 8 * 1024 * 1024:
            raise serializers.ValidationError(
                detail="The file is too large. What were you uploading? The max file size is 8 MB!",
                code="file_size_exceeded",
            )

        image = Image.open(file_bytes)
        image.verify()

        if image.format.lower() not in ["jpeg", "png", "webp", "jfif", "avif", "bmp"]:
            raise serializers.ValidationError(
                detail="The uploaded image's format is not supported. Is it even an image?",
                code="invalid_file_format",
            )

        instance.file = File(file_bytes, name="image.webp")
        instance.verification_status = Image.VerificationStatus.NOT_REVIEWED
        instance.save()

        image.close()

        return HttpResponse("", status=204)


class ImageRelationshipsView(views.RelationshipView):
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Image.objects.all()
        return Image.objects.filter(
            verification_status=Image.VerificationStatus.VERIFIED
        )

    def get_permissions(self):
        if self.request.method != "GET":
            return [permissions.IsAdminUser]
        return []


class ImageEmbedView(View):
    @method_decorator(xframe_options_exempt)
    def get(self, request, pk):
        """
        Returns the rendered embed of an image.
        """

        image = get_object_or_404(Image, pk=pk)

        return render(request, "images/embeds/image.html", context={"image": image})
