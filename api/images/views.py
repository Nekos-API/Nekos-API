from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_json_api import views, serializers

from django_ratelimit.decorators import ratelimit

from utils.decorators import permission_classes

from .models import Image
from .serializers import ImageSerializer


@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="list")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="retrieve")
@method_decorator(
    ratelimit(group="api", key="user_or_ip", rate="1/s"), name="retrieve_related"
)
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="create")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="update")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="delete")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="like")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="unlike")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="save")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="unsave")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="verify")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="unverify")
class ImagesViewSet(views.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filterset_fields = {
        "id": ("exact", "in", "regex", "iregex"),
        "age_rating": ("iexact", "exact", "in", "isnull", "regex", "iregex"),
        "height": ("exact", "lt", "lte", "gt", "gte"),
        "width": ("exact", "lt", "lte", "gt", "gte"),
        "aspect_ratio": ("exact", "startswith", "endswith", "regex"),
        "is_original": ("exact", "isnull"),
        "is_verified": ("exact",),
        "source_name": ("iexact", "exact", "contains", "icontains", "startswith", "endswith", "isnull", "regex", "iregex"),
        "source_url": ("iexact", "exact", "contains", "icontains", "startswith", "endswith", "isnull", "regex", "iregex"),
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
        "is_verified",
    ]

    @permission_classes([permissions.IsAuthenticated])
    def create(self, request, *args, **kwargs):
        """
        Creates a new unverified image.
        """
        return super().create(request, *args, **kwargs)

    @permission_classes([permissions.IsAuthenticated])
    def update(self, request, *args, **kwargs):
        """
        Updates an existent image.
        """

        image = get_object_or_404(
            Image.objects.select_related("uploader"), pk=kwargs.get("pk")
        )

        if not request.user.is_superuser:
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

        image = get_object_or_404(Image.objects.select_related("uploader"), pk=pk)

        if not request.user.is_superuser:
            if request.user != image.uploader:
                raise serializers.ValidationError(
                    detail="You cannot delete an image that you have not originally posted.",
                    code="cannot_delete_unowned_image",
                )

        image.delete()

        return Response(data="", status=204)

    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    def verify(self, request, pk):
        """
        Verify an image.
        """

        image = get_object_or_404(Image, pk=pk)
        image.is_verified = True
        image.save()

        return Response(ImageSerializer(image, context={"request": "request"}).data)

    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    def unverify(self, request, pk):
        """
        Set an image as not verified.
        """

        image = get_object_or_404(Image, pk=pk)
        image.is_verified = False
        image.save()

        return Response(ImageSerializer(image, context={"request": "request"}).data)

    @permission_classes([permissions.IsAuthenticated])
    def like(self, request, *args, **kwargs):
        """
        Add image to liked images.
        """

        image = self.get_object()

        if image.liked_by.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                code="image_already_liked", detail="You have already liked this image."
            )

        request.user.liked_images.add(image)

        return HttpResponse("", status=204)

    @permission_classes([permissions.IsAuthenticated])
    def unlike(self, request, *args, **kwargs):
        """
        Remove image from liked images.
        """

        image = self.get_object()

        if not image.liked_by.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                code="image_not_liked", detail="You have not liked this image yet."
            )

        request.user.liked_images.remove(image)

        return HttpResponse("", status=204)

    @permission_classes([permissions.IsAuthenticated])
    def save(self, request, *args, **kwargs):
        """
        Add image to saved images.
        """

        image = self.get_object()

        if image.saved_by.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                code="image_already_saved", detail="You have already saved this image."
            )

        request.user.saved_images.add(image)

        return HttpResponse("", status=204)

    @permission_classes([permissions.IsAuthenticated])
    def unsave(self, request, *args, **kwargs):
        """
        Remove image from saved images.
        """

        image = self.get_object()

        if not image.saved_by.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                code="image_not_saved", detail="You have not saved this image yet."
            )

        request.user.saved_images.remove(image)

        return HttpResponse("", status=204)


@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="get")
class ImageRelationshipsView(views.RelationshipView):
    queryset = Image.objects
