import re

from rest_framework_json_api import serializers, relations

from images.models import Image
from characters.models import Character
from categories.models import Category
from artists.models import Artist
from lists.models import List

from .models import User, DiscordUser


class NameSerializer(serializers.Serializer):
    first = serializers.CharField(source="first_name")
    last = serializers.CharField(source="last_name")


class PermissionsSerializer(serializers.Serializer):
    isActive = serializers.BooleanField(source="is_active")
    isStaff = serializers.BooleanField(source="is_staff")
    isSuperuser = serializers.BooleanField(source="is_superuser")


class TimestampsSerializer(serializers.Serializer):
    joined = serializers.DateTimeField(source="date_joined")


class TimestampsPrivateSerializer(TimestampsSerializer):
    lastLogin = serializers.DateTimeField(source="last_login")


class UserPublicSerializer(serializers.HyperlinkedModelSerializer):
    included_serializers = {
        "following": "users.serializers.UserPublicSerializer",
        "followers": "users.serializers.UserPublicSerializer",
        "followed_artists": "artists.serializers.ArtistSerializer",
        "followed_characters": "characters.serializers.CharacterSerializer",
        "followed_categories": "categories.serializers.CategorySerializer",
        "followed_lists": "lists.serializers.ListSerializer",
    }

    class Meta:
        model = User
        fields = [
            "username",
            "nickname",
            "biography",
            "avatar_image",
            "timestamps",
            "permissions",
            "following",
            "followers",
            "followed_artists",
            "followed_characters",
            "followed_categories",
            "followed_lists",
            "user",
            "url",
        ]
        extra_kwargs = {
            "avatar_image": {"read_only": True},
            "permissions": {"read_only": True},
        }
        meta_fields = ["user"]

    def username_validator(value):
        if len(value) < 4:
            raise serializers.ValidationError(
                detail="The username cannot be shorten than 4 characters.",
                code="username_too_short",
            )
        elif len(value) > 32:
            raise serializers.ValidationError(
                detail="The username cannot be longer than 32 characters (which is anyways too long for a username).",
                code="username_too_long",
            )
        elif re.match(r"^([0-9]|[a-z]|_|\.)+$", value) is None:
            raise serializers.ValidationError(
                detail="The username contains invalid characters.",
                code="invalid_characters",
            )

    username = serializers.CharField(required=False)
    permissions = PermissionsSerializer(source="*", read_only=True)
    timestamps = TimestampsSerializer(source="*", read_only=True)
    following = relations.ResourceRelatedField(
        many=True,
        read_only=True,
        related_link_view_name="user-related",
        self_link_view_name="user-relationships",
    )
    followers = relations.ResourceRelatedField(
        many=True,
        read_only=True,
        related_link_view_name="user-related",
        self_link_view_name="user-relationships",
    )
    followed_characters = relations.ResourceRelatedField(
        many=True,
        read_only=True,
        related_link_view_name="user-related",
        self_link_view_name="user-relationships",
    )
    followed_categories = relations.ResourceRelatedField(
        many=True,
        read_only=True,
        related_link_view_name="user-related",
        self_link_view_name="user-relationships",
    )
    followed_artists = relations.ResourceRelatedField(
        many=True,
        read_only=True,
        related_link_view_name="user-related",
        self_link_view_name="user-relationships",
    )
    followed_lists = relations.ResourceRelatedField(
        many=True,
        read_only=True,
        related_link_view_name="user-related",
        self_link_view_name="user-relationships",
    )

    user = serializers.SerializerMethodField(method_name="get_user_meta")

    def get_user_meta(self, obj):
        if self.context["request"].user.is_authenticated:
            follower_pks = list(obj.followers.values_list("pk", flat=True))
            following_pks = list(obj.following.values_list("pk", flat=True))
            return {
                "isFollowing": self.context["request"].user.pk in follower_pks,
                "isBeingFollowed": self.context["request"].user.pk in following_pks,
            }
        return {"isFollowing": None, "isBeingFollowed": None}


class UserPrivateSerializer(UserPublicSerializer):
    included_serializers = {
        "liked_images": "images.serializers.ImageSerializer",
        "following": "users.serializers.UserPublicSerializer",
        "followers": "users.serializers.UserPublicSerializer",
        "followed_artists": "artists.serializers.ArtistSerializer",
        "followed_characters": "characters.serializers.CharacterSerializer",
        "followed_categories": "categories.serializers.CategorySerializer",
        "discord": "users.serializers.DiscordUserSerializer",
    }

    class Meta:
        model = User
        fields = [
            "username",
            "name",
            "nickname",
            "biography",
            "avatar_image",
            "email",
            "secret_key",
            "following",
            "followers",
            "permissions",
            "timestamps",
            "followed_artists",
            "followed_characters",
            "followed_categories",
            "liked_images",
            "saved_images",
            "discord",
            "user",
            "url",
        ]
        extra_kwargs = {
            "avatar_image": {"read_only": True},
            "permissions": {"read_only": True},
            "secret_key": {"read_only": True},
        }
        meta_fields = ["user"]

    name = NameSerializer(source="*", required=False)
    email = serializers.EmailField(required=False)
    liked_images = relations.ResourceRelatedField(
        many=True,
        read_only=True,
        related_link_view_name="user-related",
        self_link_view_name="user-relationships",
    )
    saved_images = relations.ResourceRelatedField(
        many=True,
        read_only=True,
        related_link_view_name="user-related",
        self_link_view_name="user-relationships",
    )
    discord = relations.ResourceRelatedField(
        read_only=True,
        related_link_view_name="user-related",
        self_link_view_name="user-relationships",
    )


class DiscordUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscordUser
        fields = ["email"]
