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
            "user",
            "url",
        ]
        meta_fields = ["user"]

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

    user = serializers.SerializerMethodField(method_name="get_user_meta")

    def get_user_meta(self, obj):
        """
        Returns metadata related to the user, e.g. isFollowing.
        """
        if self.context["request"].user.is_authenticated:
            follower_pks = list(obj.followers.values_list("pk", flat=True))
            return {"isFollowing": self.context["request"].user.pk in follower_pks}
        return {"isFollowing": None}
