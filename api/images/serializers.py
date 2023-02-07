"""
Note: in nested serializers (ColorsSerializer, SourceSerializer, etc.) field
camelization does not work. You'll have to manually change the field names to
keep the responses consistent.
"""

from rest_framework_json_api import serializers, relations

from categories.models import Category
from categories.serializers import CategorySerializer
from artists.models import Artist
from artists.serializers import ArtistSerializer
from characters.models import Character
from characters.serializers import CharacterSerializer
from users.models import User
from users.serializers import UserPublicSerializer

from .models import Image


class ColorsSerializer(serializers.Serializer):
    primary = serializers.SerializerMethodField()
    dominant = serializers.SerializerMethodField()

    def get_primary(self, obj):
        """
        Parses r,g,b db array to hex color code
        """
        return (
            "#{:02x}{:02x}{:02x}".format(*obj.primary_color)
            if obj.primary_color
            else None
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

    name = serializers.CharField(source="source_name")
    url = serializers.CharField(source="source_url")


class DimensionsSerializer(serializers.Serializer):
    """
    Serializes the image's dimensions into an object.
    """

    height = serializers.IntegerField()
    width = serializers.IntegerField()
    aspectRatio = serializers.CharField(source="aspect_ratio")


class TimestampsSerializer(serializers.Serializer):
    """
    Serializes the created_at and updated_at fields into an object.
    """

    created = serializers.DateTimeField(source="created_at")
    updated = serializers.DateTimeField(source="updated_at")


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    """
    Converts an Image object into JSON:API data.
    """

    included_serializers = {
        "artist": ArtistSerializer,
        "categories": CategorySerializer,
        "characters": CharacterSerializer,
        "liked_by": UserPublicSerializer,
        "uploader": UserPublicSerializer,
    }

    class Meta:
        model = Image
        fields = [
            "file",
            "title",
            "colors",
            "source",
            "dimens",
            "is_original",
            "is_verified",
            "age_rating",
            "timestamps",
            "uploader",
            "artist",
            "categories",
            "characters",
            "liked_by",
            "url",
        ]

    class JSONAPIMeta:
        included_resources = ["artist"]

    def age_rating_validator(value):
        """
        Validate age rating value.
        """
        if value not in ["sfw", "questionable", "borderline", "explicit"]:
            raise serializers.ValidationError(
                detail="Age rating is not valid.", code="invalid_age_rating"
            )

    def validate(self, attrs):
        """
        Set the uploader to the user itself.
        """

        attrs["uploader"] = self.context["request"].user
        return attrs

    colors = ColorsSerializer(source="*", read_only=True)
    source = SourceSerializer(source="*", required=True)
    dimens = DimensionsSerializer(source="*", read_only=True)
    is_original = serializers.BooleanField(required=True)
    age_rating = serializers.CharField(required=True, validators=[age_rating_validator])
    timestamps = TimestampsSerializer(source="*", read_only=True)
    uploader = relations.ResourceRelatedField(
        related_link_view_name="image-related",
        self_link_view_name="image-relationships",
        read_only=True,
    )
    artist = relations.ResourceRelatedField(
        queryset=Artist.objects,
        related_link_view_name="image-related",
        self_link_view_name="image-relationships",
    )
    categories = relations.ResourceRelatedField(
        queryset=Category.objects,
        many=True,
        related_link_view_name="image-related",
        self_link_view_name="image-relationships",
        required=True,
    )
    characters = relations.ResourceRelatedField(
        queryset=Character.objects,
        many=True,
        related_link_view_name="image-related",
        self_link_view_name="image-relationships",
        required=False,
    )
    liked_by = relations.ResourceRelatedField(
        many=True,
        read_only=True,
        related_link_view_name="image-related",
        self_link_view_name="image-relationships",
    )
