from rest_framework_json_api import serializers, relations

from images.models import Image
from users.models import User

from .models import List


class TimestampsSerializer(serializers.Serializer):
    created = serializers.DateTimeField(source="created_at")
    updated = serializers.DateTimeField(source="updated_at")


class ListSerializer(serializers.HyperlinkedModelSerializer):
    included_serializers = {
        "images": "images.serializers.ImageSerializer",
        "user": "users.serializers.UserPublicSerializer",
        "followers": "users.serializers.UserPublicSerializer",
    }

    class Meta:
        model = List
        fields = [
            "name",
            "description",
            "is_private",
            "timestamps",
            "user",
            "images",
            "followers",
            "url",
        ]

    def validate(self, attrs):
        """
        Set the user to the user that created the list.
        """
        attrs["user"] = self.context["request"].user
        return attrs

    user = relations.ResourceRelatedField(
        related_link_view_name="list-related",
        self_link_view_name="list-relationships",
        read_only=True
    )
    images = relations.ResourceRelatedField(
        queryset=Image.objects,
        many=True,
        related_link_view_name="list-images-list",
        self_link_view_name="list-relationships",
    )
    followers = relations.ResourceRelatedField(
        many=True,
        related_link_view_name="list-related",
        self_link_view_name="list-relationships",
        read_only=True,
    )

    timestamps = TimestampsSerializer(source="*", read_only=True)
