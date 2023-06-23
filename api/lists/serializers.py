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
        "owner": "users.serializers.UserPublicSerializer",
        "followers": "users.serializers.UserPublicSerializer",
    }

    class Meta:
        model = List
        fields = [
            "name",
            "description",
            "is_private",
            "timestamps",
            "owner",
            "images",
            "followers",
            "user",
            "url",
        ]
        meta_fields = [
            "user"
        ]

    def validate(self, attrs):
        """
        Set the user to the user that created the list.
        """
        attrs["owner"] = self.context["request"].user
        return attrs

    owner = relations.ResourceRelatedField(
        related_link_view_name="list-related",
        self_link_view_name="list-relationships",
        read_only=True,
        source="user"
    )
    images = relations.ResourceRelatedField(
        queryset=Image.objects,
        many=True,
        related_link_view_name="list-related",
        self_link_view_name="list-relationships",
    )
    followers = relations.ResourceRelatedField(
        many=True,
        related_link_view_name="list-related",
        self_link_view_name="list-relationships",
        read_only=True,
    )

    timestamps = TimestampsSerializer(source="*", read_only=True)

    user = serializers.SerializerMethodField(method_name="get_user_meta")

    def get_user_meta(self, obj):
        """
        Returns metadata related to the user, e.g. isFollowing.
        """
        if self.context["request"].user.is_authenticated:
            follower_pks = list(obj.followers.values_list("pk", flat=True))
            return {
                "isFollowing": self.context["request"].user.pk in follower_pks
            }
        return {
            "isFollowing": None
        }
