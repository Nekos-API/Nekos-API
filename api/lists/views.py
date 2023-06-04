from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from rest_framework import serializers, permissions, exceptions
from rest_framework.response import Response
from rest_framework_json_api import views

from utils.decorators import permission_classes

from django_ratelimit.decorators import ratelimit

from images.models import Image

from .models import List
from .serializers import ListSerializer

# Create your views here.


class ListViewSet(views.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    select_for_includes = {"user": ["user"]}
    prefetch_for_includes = {
        "images": ["images"],
        "followers": ["followers"],
    }

    @permission_classes([permissions.IsAuthenticated])
    def create(self, request, *args, **kwargs):
        """
        Create a new list.
        """
        return super().create(request, *args, **kwargs)

    @permission_classes([permissions.IsAuthenticated])
    def update(self, request, *args, **kwargs):
        """
        Updates an existent image.
        """

        images_list = get_object_or_404(
            List.objects.select_related("user"), pk=kwargs.get("pk")
        )

        if not request.user.is_superuser:
            if request.user != images_list.user:
                raise serializers.ValidationError(
                    detail="You cannot update a list that you do not own.",
                    code="cannot_update_unowned_list",
                )

        return super().update(request, *args, **kwargs)

    @permission_classes([permissions.IsAuthenticated])
    def delete(self, request, pk):
        """
        Delete an image.
        """

        images_list = get_object_or_404(List.objects.select_related("user"), pk=pk)

        if not request.user.is_superuser:
            if request.user != images_list.user:
                raise serializers.ValidationError(
                    detail="You cannot delete a list that you do not own.",
                    code="cannot_delete_unowned_list",
                )

        images_list.delete()

        return Response(data="", status=204)

    @permission_classes([permissions.IsAuthenticated])
    def follow(self, request, *args, **kwargs):
        """
        Add list to followed lists.
        """

        image_lists = self.get_object()

        if image_lists.followed_lists.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                {
                    "id": "list_already_followed",
                    "detail": "You are already following this list.",
                    "source": {
                        "pointer": "/data",
                    },
                }
            )

        request.user.followed_lists.add(image_lists)

        return HttpResponse("", status=204)

    @permission_classes([permissions.IsAuthenticated])
    def unfollow(self, request, *args, **kwargs):
        """
        Remove list from followed lists.
        """

        image_lists = self.get_object()

        if not image_lists.followed_lists.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                detail="You are not following this list",
                code="list_not_followed",
            )

        request.user.followed_lists.remove(image_lists)

        return HttpResponse("", status=204)


class ListRelationshipsView(views.RelationshipView):
    queryset = List.objects.all()

    def check_write_permission(self):
        """
        Check wether the current user has write permission or not. Raises
        `PermissionDenied` error in case the user does not have it.
        """
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            if self.kwargs.get("related_field") != "images":
                raise exceptions.PermissionDenied()
            obj = self.get_object()
            if obj.user != self.request.user:
                raise exceptions.PermissionDenied()

    def post(self, request, *args, **kwargs):
        self.check_write_permission()
        return super().post(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.check_write_permission()
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.check_write_permission()
        return super().delete(request, *args, **kwargs)
