from rest_framework_json_api import serializers, relations

from images.models import Image
from users.models import User

from .models import Character


class NameSerializer(serializers.Serializer):
    first = serializers.CharField(source="first_name")
    last = serializers.CharField(source="last_name")
    aliases = serializers.ListField()


class TimestampsSerializer(serializers.Serializer):
    created = serializers.DateTimeField(source="created_at")
    updated = serializers.DateTimeField(source="updated_at")


class CharacterSerializer(serializers.ModelSerializer):
    included_serializers = {
        "images": "images.serializers.ImageSerializer",
        "followers": "users.serializers.UserPublicSerializer",
    }

    class Meta:
        model = Character
        fields = [
            "id",
            "name",
            "description",
            "gender",
            "species",
            "ages",
            "birth_date",
            "nationality",
            "occupations",
            "timestamps",
            "images",
            "followers",
            "url",
        ]

    name = NameSerializer(source="*")
    description = serializers.CharField()
    gender = serializers.CharField()
    species = serializers.CharField()
    ages = serializers.ListField()
    birth_date = serializers.CharField()
    nationality = serializers.CharField()
    occupations = serializers.ListField()
    timestamps = TimestampsSerializer(source="*")
    images = relations.ResourceRelatedField(
        model=Image,
        queryset=Image.objects,
        many=True,
        related_link_view_name="character-related",
        self_link_view_name="character-relationships",
    )
    followers = relations.ResourceRelatedField(
        model=User,
        queryset=User.objects,
        many=True,
        related_link_view_name="character-related",
        self_link_view_name="character-relationships",
    )
