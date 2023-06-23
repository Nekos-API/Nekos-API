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


class DimensionsSerializer(serializers.Serializer):
    """
    Serializes the image's dimensions into an object.
    """

    height = serializers.IntegerField()
    width = serializers.IntegerField()
    aspectRatio = serializers.CharField(source="aspect_ratio")
    orientation = serializers.CharField()


class MetadataSerializer(serializers.Serializer):
    """
    Serializes `mimetype` and `fileSize` into an object.
    """
    mimetype = serializers.CharField()
    fileSize = serializers.IntegerField(source="file_size")


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
            "verification_status",
            "age_rating",
            "metadata",
            "timestamps",
            "uploader",
            "artist",
            "categories",
            "characters",
            "liked_by",
            "user",
            "url",
        ]
        extra_kwargs = {
            "is_original": {"required": True},
            "verification_status": {"read_only": True},
            "file": {"read_only": True},
        }
        meta_fields = [
            "user"
        ]

    class JSONAPIMeta:
        included_resources = ["artist"]

    def age_rating_validator(value):
        """
        Validate age rating value.
        """
        if value not in ["sfw", "questionable", "suggestive", "borderline", "explicit"]:
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
    source = SourceSerializer(source="*", read_only=True)
    dimens = DimensionsSerializer(source="*", read_only=True)
    age_rating = serializers.CharField(required=True, validators=[age_rating_validator])
    timestamps = TimestampsSerializer(source="*", read_only=True)
    metadata = MetadataSerializer(source="*", read_only=True)
    uploader = relations.ResourceRelatedField(
        related_link_view_name="image-related",
        self_link_view_name="image-relationships",
        read_only=True,
    )
    artist = relations.ResourceRelatedField(
        queryset=Artist.objects,
        related_link_view_name="image-related",
        self_link_view_name="image-relationships",
        required=False,
        allow_null=True,
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

    user = serializers.SerializerMethodField(method_name="get_user_meta")

    def get_user_meta(self, obj):
        """
        Returns metadata related to the user, e.g. isFollowing.
        """
        if self.context["request"].user.is_authenticated:
            liked_by_pks = list(obj.liked_by.values_list("pk", flat=True))
            saved_by_pks = list(obj.saved_by.values_list("pk", flat=True))
            return {
                "liked": self.context["request"].user.pk in liked_by_pks,
                "saved": self.context["request"].user.pk in saved_by_pks,
            }
        return {
            "liked": None,
            "saved": None
        }
