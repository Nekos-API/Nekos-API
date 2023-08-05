"""
Note: in nested serializers (ColorsSerializer, SourceSerializer, etc.) field
camelization does not work. You'll have to manually change the field names to
keep the responses consistent.
"""
from urllib.parse import urlparse

from django.core.files.storage import default_storage

from rest_framework_json_api import serializers, relations

from characters.models import Character
from characters.serializers import CharacterSerializer

from categories.models import Category
from categories.serializers import CategorySerializer

from users.models import User
from users.serializers import UserPublicSerializer

from .models import Gif, Reaction


class DimensSerializer(serializers.Serializer):
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    aspectRatio = serializers.FloatField(source="aspect_ratio")
    orientation = serializers.CharField()


class MetadataSerializer(serializers.Serializer):
    mimetype = serializers.CharField()
    size = serializers.IntegerField(source="file_size")
    frames = serializers.IntegerField()
    duration = serializers.IntegerField()


class ColorsSerializer(serializers.Serializer):
    dominant = serializers.SerializerMethodField()
    palette = serializers.SerializerMethodField()

    def get_palette(self, obj):
        """
        Parses r,g,b db array to hex color code
        """
        return (
            [
                ("#{:02x}{:02x}{:02x}".format(*color) if color else None)
                for color in obj.palette
            ]
            if obj.palette
            else []
        )

    def get_dominant(self, obj):
        """
        Parses r,g,b db array to hex color code
        """
        return (
            "#{:02x}{:02x}{:02x}".format(*obj.dominant_color)
            if obj.dominant_color
            else None
        )


class SourceSerializer(serializers.Serializer):
    """
    Serializes the image's source into an object.
    """

    name = serializers.CharField(source="source_name", required=False)
    url = serializers.CharField(source="source_url", required=False)


class TimestampsSerializer(serializers.Serializer):
    """
    Serializes the created_at and updated_at fields into an object.
    """

    created = serializers.DateTimeField(source="created_at")
    updated = serializers.DateTimeField(source="updated_at")


class GifSerializer(serializers.ModelSerializer):
    included_serializers = {
        "categories": CategorySerializer,
        "characters": CharacterSerializer,
        "uploader": UserPublicSerializer,
        "reactions": "gifs.serializers.ReactionSerializer",
    }

    class Meta:
        model = Gif
        fields = [
            "file",
            "text",
            "colors",
            "source",
            "verification_status",
            "age_rating",
            "is_spoiler",
            "emotions",
            "dimens",
            "metadata",
            "timestamps",
            "reactions",
            "characters",
            "categories",
            "uploader",
            "url",
        ]

    class JSONAPIMeta:
        included_resources = ["reactions"]

    colors = ColorsSerializer(source="*")
    source = SourceSerializer(source="*")
    dimens = DimensSerializer(source="*")
    metadata = MetadataSerializer(source="*")
    timestamps = TimestampsSerializer(source="*")

    reactions = relations.ResourceRelatedField(
        queryset=Reaction.objects,
        many=True,
        related_link_view_name="gif-related",
        self_link_view_name="gif-relationships",
        required=False,
    )
    uploader = relations.ResourceRelatedField(
        related_link_view_name="gif-related",
        self_link_view_name="gif-relationships",
        read_only=True,
    )
    categories = relations.ResourceRelatedField(
        queryset=Category.objects,
        many=True,
        related_link_view_name="gif-related",
        self_link_view_name="gif-relationships",
        required=True,
    )
    characters = relations.ResourceRelatedField(
        queryset=Character.objects,
        many=True,
        related_link_view_name="gif-related",
        self_link_view_name="gif-relationships",
        required=False,
    )


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = [
            "name",
            "is_nsfw",
        ]
