from datetime import timedelta, datetime

from tempfile import NamedTemporaryFile

import os

import urllib

import secrets

import json

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.files import File
from django.views.generic import View
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import exceptions, permissions, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_json_api import views, serializers

from oauth2_provider.models import AccessToken, RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views import AuthorizationView
from oauth2_provider.views.mixins import OAuthLibMixin, OIDCOnlyMixin

from oauthlib import common

from jwcrypto import jwk

from django_ratelimit.decorators import ratelimit

from PIL import Image

import requests

import dotenv

from utils import get_or_none
from utils.decorators import permission_classes

from applications.models import Application

from .models import User, DiscordUser
from .serializers import UserPublicSerializer, UserPrivateSerializer

dotenv.load_dotenv()

# Create your views here.


def get_client_ip(request) -> str:
    """
    Returns the original client IP.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def validate_recaptcha(request) -> bool:
    """
    Validates a reCAPTCHA challenge and returns wether it has been successful
    or not.
    """
    r = requests.post(
        "https://www.google.com/recaptcha/api/siteverify?"
        + urllib.parse.urlencode(
            {
                "response": request.POST.get("g-recaptcha-response"),
                "secret": os.getenv("RECAPTCHA_SECRET_KEY"),
                "remoteip": get_client_ip(request),
            }
        )
    )
    return r.json()["success"]


class UserView(views.ModelViewSet):
    queryset = User.objects.all()
    select_for_includes = {"discord": ["discord"]}
    prefetch_for_includes = {
        "liked_images": ["liked_images"],
        "saved_images": ["saved_images"],
        "following": ["following"],
        "followed": ["followed"],
        "followed_artists": ["followed_artists"],
        "followed_characters": ["followed_characters"],
        "followed_categories": ["followed_categories"],
        "followed_lists": ["followed_lists"],
    }
    filterset_fields = {"discord__id": ["exact"]}

    def get_serializer_class(self):
        if (
            (self.request.user.is_authenticated and self.kwargs.get("pk") == "@me")
            or (
                self.request.user.is_authenticated
                and str(self.kwargs.get("pk")) == str(self.request.user.id)
            )
            or (self.request.user.is_authenticated and self.request.user.is_superuser)
        ):
            return UserPrivateSerializer
        return UserPublicSerializer

    def get_object(self):
        if (self.request.user.is_authenticated and self.kwargs.get("pk") == "@me") or (
            self.request.user.is_authenticated
            and self.kwargs.get("pk") == str(self.request.user.id)
        ):
            return self.request.user
        elif not self.request.user.is_authenticated and self.kwargs.get("pk") == "@me":
            raise exceptions.NotAuthenticated()
        else:
            return User.objects.get(pk=self.kwargs.get("pk"))

    def signup(self, request):
        """
        Sign up a user.
        """

        if (
            request.headers.get("Authorization")
            != "Token " + settings.PROTECTED_API_TOKEN
        ):
            return HttpResponse(content="", status=401)

        user = User(
            username=request.POST.get("username"),
            email=request.POST.get("email"),
            first_name=request.POST.get("firstName"),
            last_name=request.POST.get("lastName"),
            is_active=False,
        )
        user.set_password(request.POST.get("password"))
        user.save()

        return Response(UserPrivateSerializer(data=user))

    @permission_classes([permissions.IsAuthenticated])
    def update(self, request, *args, **kwargs):
        """
        Edit a user.
        """

        user = self.get_object()

        if request.user != user:
            raise serializers.ValidationError(
                detail="You cannot update another user's data!",
                code="cannot_update_unauthenticated_user",
            )

        response = super().update(request, *args, **kwargs)

        response.headers[
            "X-Avatar-Upload-Location"
        ] = "https://api.nekosapi.com/v2/users/@me/avatar"

        return response

    def retrieve_related(self, request, pk, related_field, *args, **kwargs):
        """
        Verifies that the request is not trying to access private
        endpoints.
        """
        if related_field in ["saved-images", "discord"]:
            if not request.user.is_authenticated:
                raise exceptions.NotAuthenticated()
            elif str(request.user.pk) != str(pk):
                raise serializers.ValidationError(
                    detail="You cannot see this information.", code="forbidden"
                )

        return super().retrieve_related(
            request, pk=pk, related_field=related_field, *args, **kwargs
        )

    @permission_classes([permissions.IsAuthenticated])
    def follow(self, request, *args, **kwargs):
        """
        Follow a user.
        """

        user = self.get_object()

        if user == request.user:
            raise serializers.ValidationError(
                {
                    "id": "self_follow_forbidden",
                    "detail": "You followed yourself. Wait, you cannot.",
                    "source": {
                        "pointer": "/data",
                    },
                }
            )

        if user.followers.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                {
                    "id": "user_already_followed",
                    "detail": "You are already following the user.",
                    "source": {
                        "pointer": "/data",
                    },
                }
            )

        request.user.following.add(user)

        return HttpResponse("", status=204)

    @permission_classes([permissions.IsAuthenticated])
    def unfollow(self, request, *args, **kwargs):
        """
        Unfollow a user.
        """

        user = self.get_object()

        if user == request.user:
            raise serializers.ValidationError(
                {
                    "id": "self_follow_forbidden",
                    "detail": "You cannot unfollow yourself.",
                    "source": {
                        "pointer": "/data",
                    },
                }
            )

        if not user.followers.filter(pk=request.user.pk).exists():
            raise serializers.ValidationError(
                {
                    "id": "user_not_followed",
                    "detail": "You are not following this user.",
                    "source": {
                        "pointer": "/data",
                    },
                }
            )

        request.user.following.remove(user)

        return HttpResponse("", status=204)


class UserAdminViewSet(ViewSet):
    @permission_classes([permissions.IsAdminUser])
    def create_token(self, request, pk):
        """
        Creates an access and a refresh token for a specific user.
        """

        user = get_object_or_404(User, pk=pk)

        application = Application.objects.get(pk=1)

        refresh_token = RefreshToken.objects.create(
            user=user,
            application=application,
            token=secrets.token_urlsafe(20),
        )

        access_token = AccessToken.objects.create(
            user=user,
            application=application,
            source_refresh_token=refresh_token,
            token=secrets.token_urlsafe(20),
            expires=datetime.utcnow() + timedelta(hours=1),
        )

        return HttpResponse(
            content=json.dumps(
                {
                    "data": {
                        "type": "token",
                        "id": None,
                        "attributes": {
                            "access": access_token.token,
                            "refresh": refresh_token.token,
                        },
                    }
                }
            ),
            content_type="application/vnd.api+json",
        )


class UserAvatarUploadView(APIView):
    """
    This view handles the user avatar image upload.
    """

    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        """
        Handle the file upload.
        """

        file_bytes = request.data["file"].file

        # Prevent from uploading files > 2 MB size
        if file_bytes.getbuffer().nbytes > 2097152:
            raise serializers.ValidationError(
                detail="The file is too large. What were you uploading? The max file size is 2 MB!",
                code="file_size_exceeded",
            )

        image = Image.open(file_bytes)
        image.verify()

        if image.format.lower() not in ["jpeg", "png", "webp", "jfif", "avif", "bmp"]:
            raise serializers.ValidationError(
                detail="The uploaded image's format is not supported. Is it even an image?",
                code="invalid_file_format",
            )

        request.user.avatar_image = File(file_bytes, name="avatar.webp")
        request.user.save()

        image.close()

        return HttpResponse("", status=204)


class UserRelationshipsView(views.RelationshipView):
    queryset = User.objects.all()

    def get_object(self):
        if (self.request.user.is_authenticated and self.kwargs.get("pk") == "@me") or (
            isinstance(self.request.user, User)
            and self.kwargs.get("pk") == str(self.request.user.id)
        ):
            return self.request.user
        elif not self.request.user.is_authenticated and self.kwargs.get("pk") == "@me":
            raise exceptions.NotAuthenticated()
        else:
            return User.objects.get(pk=self.kwargs.get("pk"))

    def check_write_permission(self):
        """
        Check wether the current user has write permission or not. Raises
        `PermissionDenied` error in case the user does not have it.
        """
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            if self.kwargs.get("related_field") not in [
                "liked-images",
                "saved-images",
                "followed-characters",
                "followed-artists",
                "followed-categories",
                "followed-lists",
                "following",
            ]:
                raise exceptions.PermissionDenied()
            user = self.get_object()
            if user != self.request.user:
                raise exceptions.PermissionDenied()
        raise exceptions.PermissionDenied()

    def get(self, request, pk, related_field, *args, **kwargs):
        """
        Verifies that the request is not trying to access private
        endpoints.
        """
        if related_field in ["saved-images", "discord"]:
            if not request.user.is_authenticated:
                raise exceptions.NotAuthenticated()
            elif str(request.user.pk) != str(pk):
                raise exceptions.PermissionDenied()

        return super().get(request, pk=pk, related_field=related_field, *args, **kwargs)

    def post(self, *args, **kwargs):
        self.check_write_permission()
        return super().post(*args, **kwargs)

    def patch(self, *args, **kwargs):
        self.check_write_permission()
        return super().patch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.check_write_permission()
        return super().delete(*args, **kwargs)

    def get_permissions(self):
        if self.request.method != "GET":
            return [permissions.IsAuthenticated]
        return []


class AuthorizationWithCaptchaView(AuthorizationView):
    def post(self, request, *args, **kwargs):
        """
        Validate the ReCaptcha challenge.
        """

        if not validate_recaptcha(request):
            return self.get(request, *args, **kwargs)

        return super().post(request, *args, **kwargs)


class ConnectDiscoveryInfoView(OIDCOnlyMixin, View):
    """
    View used to show oidc provider configuration information
    """

    def get(self, request, *args, **kwargs):
        issuer_url = oauth2_settings.OIDC_ISS_ENDPOINT

        if not issuer_url:
            issuer_url = oauth2_settings.oidc_issuer(request)
            authorization_endpoint = request.build_absolute_uri(
                reverse("authorize")
            )
            token_endpoint = request.build_absolute_uri(
                reverse("token")
            )
            userinfo_endpoint = (
                oauth2_settings.OIDC_USERINFO_ENDPOINT
                or request.build_absolute_uri(reverse("user-info"))
            )
            jwks_uri = request.build_absolute_uri(reverse("jwks-info"))
        else:
            authorization_endpoint = "{}{}".format(
                issuer_url, reverse("authorize")
            )
            token_endpoint = "{}{}".format(issuer_url, reverse("token"))
            userinfo_endpoint = oauth2_settings.OIDC_USERINFO_ENDPOINT or "{}{}".format(
                issuer_url, reverse("user-info")
            )
            jwks_uri = "{}{}".format(issuer_url, reverse("jwks-info"))
        signing_algorithms = [Application.HS256_ALGORITHM]
        if oauth2_settings.OIDC_RSA_PRIVATE_KEY:
            signing_algorithms = [
                Application.RS256_ALGORITHM,
                Application.HS256_ALGORITHM,
            ]
        data = {
            "issuer": issuer_url,
            "authorization_endpoint": authorization_endpoint,
            "token_endpoint": token_endpoint,
            "userinfo_endpoint": userinfo_endpoint,
            "jwks_uri": jwks_uri,
            "response_types_supported": oauth2_settings.OIDC_RESPONSE_TYPES_SUPPORTED,
            "subject_types_supported": oauth2_settings.OIDC_SUBJECT_TYPES_SUPPORTED,
            "id_token_signing_alg_values_supported": signing_algorithms,
            "token_endpoint_auth_methods_supported": (
                oauth2_settings.OIDC_TOKEN_ENDPOINT_AUTH_METHODS_SUPPORTED
            ),
        }
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response
