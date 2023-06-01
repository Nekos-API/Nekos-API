"""
Note: in nested serializers (ColorsSerializer, SourceSerializer, etc.) field
camelization does not work. You'll have to manually change the field names to
keep the responses consistent.
"""

from django.core.files.storage import default_storage

from rest_framework_json_api import serializers, relations

from characters.models import Character
from characters.serializers import CharacterSerializer

from categories.models import Category
from categories.serializers import CategorySerializer

from users.models import User
from users.serializers import UserPublicSerializer

from .models import Gif, Reaction


def calculate_aspect(size: tuple, ar_size: tuple) -> tuple:
    """
    Returns a cropped size.
    """

    if size[0] in [0, None] or size[1] in [0, None]:
        return (0, 0)

    new_aspect_ratio = ar_size[0] / ar_size[1]
    current_aspect_ratio = size[0] / size[1]

    if new_aspect_ratio < current_aspect_ratio:
        # The new aspect ratio is wider than the current one.
        new_size = (size[1] / ar_size[0] * ar_size[1], size[1])

        return new_size

    elif new_aspect_ratio > current_aspect_ratio:
        # The new aspect ratio is taller than the current one.
        new_size = (size[0], size[0] / ar_size[0] * ar_size[1])

        return new_size

    else:
        # No modifications need to be done.
        return size


class FilesSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "original": {
                "url": instance.file.url,
                "dimens": {
                    "width": instance.width,
                    "height": instance.height,
                    "aspectRatio": instance.aspect_ratio,
                    "orientation": instance.orientation,
                },
                "metadata": {
                    "mimetype": instance.mimetype,
                    "size": instance.file_size,
                    "frames": instance.frames,
                    "duration": instance.duration
                },
            },
            "consistent": {
                "url": instance.file.thumbnails.consistent.url,
                "dimens": {
                    "width": calculate_aspect(
                        (instance.width, instance.height), (16, 9)
                    )[0],
                    "height": calculate_aspect(
                        (instance.width, instance.height), (16, 9)
                    )[1],
                    "aspectRatio": "16:9",
                    "orientation": "landscape",
                },
                "metadata": {
                    "mimetype": "image/gif",
                    "size": None,
                    "frames": instance.frames,
                    "duration": instance.duration
                },
            },
        }


class ColorsSerializer(serializers.Serializer):
    dominant = serializers.SerializerMethodField()
    palette = serializers.SerializerMethodField()

    def get_palette(self, obj):
        """
        Parses r,g,b db array to hex color code
        """
        return [(
            "#{:02x}{:02x}{:02x}".format(*color)
            if color
            else None
        ) for color in obj.palette] if obj.palette else []

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
            "files",
            "text",
            "colors",
            "source",
            "verification_status",
            "age_rating",
            "is_spoiler",
            "emotions",
            "timestamps",
            "reactions",
            "characters",
            "categories",
            "uploader",
            "url"
        ]

    class JSONAPIMeta:
        included_resources = ["reactions"]

    files = FilesSerializer(source="*")
    colors = ColorsSerializer(source="*")
    source = SourceSerializer(source="*")
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
