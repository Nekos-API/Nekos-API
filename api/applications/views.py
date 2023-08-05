from django.core.files import File
from django.http import HttpResponse
from django.utils.decorators import method_decorator

from rest_framework import permissions, parsers, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_json_api import views, serializers

from django_ratelimit.decorators import ratelimit

from PIL import Image

from nekos_api.permissions import IsUserAuthenticated, IsAppAuthenticated

from applications.models import Application
from applications.serializers import (
    ApplicationSerializer,
    ApplicationWithSecretSerializer,
)

from utils.decorators import permission_classes

# Create your views here.


class ApplicationView(views.ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self, *args, **kwargs):
        if IsAppAuthenticated().has_permission(self.request, self):
            return Application.objects.filter(pk=self.request.auth.application.pk)
        elif IsUserAuthenticated().has_permission(self.request, self):
            return Application.objects.filter(user=self.request.user)
        else:
            raise exceptions.NotAuthenticated()

    def get_object(self):
        if IsAppAuthenticated().has_permission(self.request, self):
            if self.kwargs.get("pk") == "@me":
                return self.request.auth.application
            return super().get_object()
        elif IsUserAuthenticated().has_permission(self.request, self):
            return super().get_object()
        else:
            raise exceptions.NotAuthenticated()

    @permission_classes([IsUserAuthenticated])
    def create(self, request):
        """
        Creates an application. By default, users are limited to 10
        applications per user to prevent spamming (since users can create
        applications 3 times per second)

        This view has a separate serializer, `ApplicationWithSecretSerializer`,
        because when an application is created users need to see the
        application's client secret.
        """

        # Users can create up to 10 applications. Superusers can skip this
        # limit.
        if request.user.applications.count() >= 10 and not request.user.is_superuser:
            raise serializers.ValidationError(
                detail="You can create up to 10 applications per user to prevent spam.",
                code="application_limit_reached",
            )

        serializer = ApplicationWithSecretSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # The user is not automatically added so it has to be added here. The
        # authorization grant type is also set to `authorization-code`
        instance = serializer.create(serializer.validated_data)
        instance.user = request.user

        # Save the client secret before hashing so that it can be returned to
        # the user.
        client_secret = instance.client_secret

        instance.save()

        # Set the client secret again to the instance (without saving) so that
        # it is serialized with the rest of the model.
        instance.client_secret = client_secret

        # Save the instance to the serializer with the saved data
        serializer.instance = instance

        return Response(serializer.data)

    @permission_classes([IsUserAuthenticated])
    def update(self, request, pk):
        """
        Update an application.
        """
        return super().update(request, pk)

    @permission_classes([IsUserAuthenticated])
    def delete(self, request, pk):
        """
        Delete an application.
        """

        application = self.get_object()

        application.delete()

        return HttpResponse("", status=204)

    def get_permissions(self):
        return [permissions.OR(IsUserAuthenticated(), IsAppAuthenticated())]


class UploadApplicationIconView(APIView):
    """
    This view handles application icon upload.
    """

    parser_classes = [parsers.MultiPartParser]
    permission_classes = [IsUserAuthenticated()]

    def get_queryset(self, *args, **kwargs):
        if IsAppAuthenticated().has_permission(self.request, self):
            return Application.objects.filter(pk=self.request.auth.application.pk)
        elif IsUserAuthenticated().has_permission(self.request, self):
            return Application.objects.filter(user=self.request.user)
        else:
            raise exceptions.NotAuthenticated()

    def get_object(self) -> Application:
        """
        Returns an Application object.
        """

        app = self.get_queryset().get(pk=int(self.kwargs.get("pk")))

        if app.user != self.request.user and not self.request.user.is_superuser:
            raise serializers.ValidationError(
                detail="You don't have permission to manage this application.",
                code="forbidden",
            )

        return app

    def put(self, request, pk):
        application = self.get_object()

        file_bytes = request.data["file"].file

        # Prevent from uploading files > 4 MB size
        if file_bytes.getbuffer().nbytes > 4 * 1024 * 1024:
            raise serializers.ValidationError(
                detail="The file is too large. What were you uploading? The max file size is 4 MB!",
                code="file_size_exceeded",
            )

        image = Image.open(file_bytes)
        image.verify()

        if image.format.lower() not in ["jpeg", "png", "webp", "jfif", "avif", "bmp"]:
            raise serializers.ValidationError(
                detail="The uploaded image's format is not supported. Is it even an image?",
                code="invalid_file_format",
            )

        application.icon = File(file_bytes, name="icon.webp")
        application.save()

        image.close()

        return HttpResponse("", status=204)
