from rest_framework_json_api import serializers, relations

from images.models import Image
from users.models import User

from .models import Category


class TimestampsSerializer(serializers.Serializer):
    created = serializers.DateTimeField(source="created_at")
    updated = serializers.DateTimeField(source="updated_at")


class CategorySerializer(serializers.ModelSerializer):
    included_serializers = {
        "images": "images.serializers.ImageSerializer",
        "followers": "users.serializers.UserPublicSerializer",
    }

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "sub",
            "is_nsfw",
            "timestamps",
            "images",
            "followers",
            "url",
        ]

    sub = serializers.CharField(source="type")
    timestamps = TimestampsSerializer(source="*")
    images = relations.ResourceRelatedField(
        queryset=Image.objects,
        many=True,
        related_link_view_name="category-related",
        self_link_view_name="category-relationships",
    )
    followers = relations.ResourceRelatedField(
        queryset=User.objects,
        many=True,
        related_link_view_name="category-related",
        self_link_view_name="category-relationships",
    )
