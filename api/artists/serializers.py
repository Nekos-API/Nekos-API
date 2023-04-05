import importlib

from rest_framework_json_api import serializers, relations

from images.models import Image
from users.models import User

from .models import Artist


class TimestampsSerializer(serializers.Serializer):
    created = serializers.DateTimeField(source="created_at")
    updated = serializers.DateTimeField(source="updated_at")


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    included_serializers = {
        "images": "images.serializers.ImageSerializer",
        "followers": "users.serializers.UserPublicSerializer",
    }

    class Meta:
        model = Artist
        fields = [
            "name",
            "aliases",
            "image_url",
            "official_links",
            "images",
            "followers",
            "url",
            "timestamps",
        ]

    name = serializers.CharField()
    image_url = serializers.URLField(source="image")
    official_links = serializers.ListField(source="links")
    images = relations.ResourceRelatedField(
        many=True,
        queryset=Image.objects,
        related_link_view_name="artist-related",
        self_link_view_name="artist-relationships",
    )
    followers = relations.ResourceRelatedField(
        many=True,
        queryset=User.objects,
        related_link_view_name="artist-related",
        self_link_view_name="artist-relationships",
    )
    timestamps = TimestampsSerializer(source="*")
