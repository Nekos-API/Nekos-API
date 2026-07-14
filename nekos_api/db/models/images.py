from enum import Enum

from datetime import datetime

from tortoise import fields
from tortoise.models import Model

from nekos_api.db.fields import NanoIDField


class Rating(str, Enum):
    SAFE = "safe"
    SUGGESTIVE = "suggestive"
    BORDERLINE = "borderline"
    EXPLICIT = "explicit"


class Image(Model):
    id: str = NanoIDField(primary_key=True)

    url: str = fields.CharField(max_length=2048)

    rating: Rating = fields.CharEnumField(Rating)

    color_primary: str = fields.CharField(max_length=7, null=True)
    color_palette: str = fields.CharField(
        max_length=7 * 10 + 9, null=True
    )  # 10 colors + 9 commas

    artist_name: str | None = fields.CharField(max_length=100, null=True)

    source_id: str | None = fields.CharField(max_length=100, null=True)
    source_url: str | None = fields.CharField(max_length=255, null=True)

    tags: fields.ManyToManyRelation["Tag"] = fields.ManyToManyField(
        "models.Tag", related_name="images"
    )

    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True)


class Tag(Model):
    id: str = NanoIDField(primary_key=True)

    name: str = fields.CharField(max_length=50, unique=True)

    is_nsfw: bool = fields.BooleanField(db_default=False)

    images: fields.ManyToManyRelation[Image]

    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True)
