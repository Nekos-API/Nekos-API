import os

import urllib

from datetime import timedelta, datetime

from tempfile import NamedTemporaryFile

import requests

import dotenv

from django.http import HttpResponse
from django.conf import settings
from django.core.files import File
from django.utils.decorators import method_decorator

from rest_framework import exceptions, permissions, viewsets, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_json_api import views, serializers

from oauth2_provider.models import AccessToken, RefreshToken, Application

from oauthlib import common

from django_ratelimit.decorators import ratelimit

from PIL import Image

from utils import get_or_none
from utils.decorators import permission_classes

from .models import User, DiscordUser
from .serializers import UserPublicSerializer, UserPrivateSerializer

dotenv.load_dotenv()

# Create your views here.


@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="list")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="retrieve")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="retrieve_related")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="update")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="follow")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="unfollow")
class UserView(views.ModelViewSet):
    queryset = User.objects.all()
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

    def get_serializer_class(self):
        if (self.request.auth and self.kwargs.get("pk") == "@me") or (
            isinstance(self.request.user, User)
            and str(self.kwargs.get("pk")) == str(self.request.user.id)
        ):
            return UserPrivateSerializer
        return UserPublicSerializer

    def get_object(self):
        if (self.request.auth and self.kwargs.get("pk") == "@me") or (
            isinstance(self.request.user, User)
            and self.kwargs.get("pk") == str(self.request.user.id)
        ):
            return self.request.user
        elif not self.request.auth and self.kwargs.get("pk") == "@me":
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


@method_decorator(ratelimit(group="api", key="ip", rate="5/m"), name="post")
class UserAvatarUploadView(APIView):
    """
    This view handles the user avatar image upload.
    """

    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle the file upload.
        """

        file_bytes = request.data["file"].file

        image = Image.open(file_bytes)
        image.verify()

        if image.format.lower() not in ["jpeg", "png", "bmp"]:
            raise serializers.ValidationError(
                detail="The uploaded image's format is not supported. Is it even an image?",
                code="invalid_file_format",
            )

        image.close()

        request.user.avatar_image = File(file_bytes, name="avatar.webp")
        request.user.save()

        return HttpResponse("", status=200)


@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="get")
class UserRelationshipsView(views.RelationshipView):
    queryset = User.objects.all()

    def get_object(self):
        if (self.request.auth and self.kwargs.get("pk") == "@me") or (
            isinstance(self.request.user, User)
            and self.kwargs.get("pk") == str(self.request.user.id)
        ):
            return self.request.user
        elif not self.request.auth and self.kwargs.get("pk") == "@me":
            raise exceptions.NotAuthenticated()
        else:
            return User.objects.get(pk=self.kwargs.get("pk"))

    def get_permissions(self):
        if self.kwargs.get("related_field") in ["liked-images", "saved-images"]:
            return [permissions.IsAuthenticated()]
        return []


class ExternalAuthAPIViewSet(viewsets.ViewSet):
    def discord(self, request):
        """
        Log in or sign up a user with Discord OAuth2.
        """

        if (
            request.headers.get("Authorization")
            != "Token " + settings.PROTECTED_API_TOKEN
        ):
            return HttpResponse(content="", status=401)

        if request.GET.get("code") is None:
            return HttpResponse(content="", status=400)

        # Get the access and refresh tokens

        data = {
            "client_id": os.getenv("DISCORD_CLIENT_ID"),
            "client_secret": os.getenv("DISCORD_CLIENT_SECRET"),
            "grant_type": "authorization_code",
            "code": request.GET.get("code"),
            "redirect_uri": os.getenv("DISCORD_REDIRECT_URI"),
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = requests.post(
            "https://discord.com/api/v10/oauth2/token",
            data=data,
            headers=headers,
            timeout=10,
        )
        r.raise_for_status()

        discord_access_token = r.json()["access_token"]
        discord_refresh_token = r.json()["refresh_token"]

        # Get the user's information

        r = requests.get(
            "https://discord.com/api/v10/users/@me",
            headers={"Authorization": "Bearer %s" % discord_access_token},
            timeout=10,
        )
        r.raise_for_status()

        user_data = r.json()

        user_avatar = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.webp?size=512"

        # Create the user in the database.

        if user_data["verified"] != True:
            # Only allow verified users
            return Response({"message": "Not verified"}, status=403)

        user = get_or_none(User, email=user_data["email"])
        discord_user = get_or_none(DiscordUser, email=user_data["email"])

        if user is None:
            # The user is not in the database (needs a sign up)

            user = User(
                username=user_data["username"] + "#" + user_data["discriminator"],
                email=user_data["email"],
            )
            user.set_unusable_password()

        if user.avatar_image is None:
            avatar_req = urllib.request.Request(
                user_avatar, headers={"User-Agent": "Nekos API"}
            )

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib.request.urlopen(avatar_req).read())
            img_temp.flush()
            user.avatar_image.save("avatar.webp", File(img_temp), save=True)

        if discord_user is None:
            discord_user = DiscordUser(
                id=int(user_data["id"]),
                email=user_data["email"],
                user=user,
                access_token=discord_access_token,
                refresh_token=discord_refresh_token,
            )
            discord_user.save()

        # Generate the access and refresh tokens

        application = Application.objects.get(pk=int(os.getenv("MAIN_APPLICATION_ID")))

        access_token = AccessToken.objects.create(
            user=user,
            expires=datetime.utcnow() + timedelta(seconds=3600),
            token=common.generate_token(),
            scope="read write groups",
            application=application,
        )
        refresh_token = RefreshToken.objects.create(
            user=user,
            application=application,
            token=common.generate_token(),
            access_token=access_token,
            revoked=datetime.utcnow() + timedelta(weeks=4),
        )

        return Response(
            {
                "type": "access",
                "id": "0",
                "attributes": {
                    "access_token": access_token.token,
                    "refresh_token": refresh_token.token,
                },
            }
        )
