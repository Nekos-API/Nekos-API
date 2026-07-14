import secrets

from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl
from pydantic_core import MISSING

from nekos_api.db import Image, Tag, Rating
from nekos_api.api.schemas import NanoID


IMAGE_URL_DESCRIPTION = "The URL of this image's file."
IMAGE_RATING_DESCRIPTION = "A rough age rating of this image. Note that most of these have been set with AI and may not be accurate."
IMAGE_COLOR_PRIMARY_DESCRIPTION = "The primary color of this image, in hex RGB format."
IMAGE_COLOR_PALETTE_DESCRIPTION = (
    "A list of UP TO 10 colors that make up this artwork's color palette, each in hex RGB format."
)
IMAGE_SOURCE_ID_DESCRIPTION = "The ID of this image on its source website, if applicable."
IMAGE_SOURCE_URL_DESCRIPTION = "The URL of this image on its source website, if applicable."
IMAGE_ARTIST_NAME_DESCRIPTION = "The name of the artist who created this image, if known."
IMAGE_TAGS_DESCRIPTION = "A list of tags associated with this image."


class ImageReadSchema(BaseModel):
    id: NanoID = Field(..., description="The unique identifier of this image.")

    url: HttpUrl = Field(..., description=IMAGE_URL_DESCRIPTION)

    rating: Rating = Field(..., description=IMAGE_RATING_DESCRIPTION)

    color_primary: str = Field(..., description=IMAGE_COLOR_PRIMARY_DESCRIPTION, example="#FF0000")
    color_palette: list[str] = Field(
        ...,
        description=IMAGE_COLOR_PALETTE_DESCRIPTION,
        example=[f"#{secrets.token_hex(3).upper()}" for _ in range(10)],
        max_length=10,
    )

    source_id: str | None = Field(..., description=IMAGE_SOURCE_ID_DESCRIPTION)
    source_url: HttpUrl | None = Field(..., description=IMAGE_SOURCE_URL_DESCRIPTION)

    artist_name: str | None = Field(..., description=IMAGE_ARTIST_NAME_DESCRIPTION)

    tags: list["TagReadSchema"] = Field(..., description=IMAGE_TAGS_DESCRIPTION)

    created_at: datetime = Field(
        ...,
        description="The date and time this image was added to the database.",
    )
    updated_at: datetime = Field(
        ...,
        description="The date and time this image was last updated in the database.",
    )

    @classmethod
    def from_orm(cls, obj: Image) -> "ImageReadSchema":
        return cls(
            id=obj.id,
            url=obj.url,
            rating=obj.rating,
            color_primary=obj.color_primary,
            color_palette=obj.color_palette.split(",") if obj.color_palette else [],
            source_id=obj.source_id,
            source_url=obj.source_url,
            artist_name=obj.artist_name,
            tags=[TagReadSchema.from_orm(tag) for tag in obj.tags],
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )


class ImageCreateSchema(BaseModel):
    url: HttpUrl = Field(..., description=IMAGE_URL_DESCRIPTION)

    rating: Rating = Field(..., description=IMAGE_RATING_DESCRIPTION)

    source_id: str | None = Field(..., description=IMAGE_SOURCE_ID_DESCRIPTION)
    source_url: HttpUrl | None = Field(..., description=IMAGE_SOURCE_URL_DESCRIPTION)

    artist_name: str | None = Field(..., description=IMAGE_ARTIST_NAME_DESCRIPTION)

    tags: list[NanoID | str] = Field(
        ...,
        description=(
            "A list of tags to associate with this image. Each item can be a tag ID or a tag "
            "name. Tag names are case-insensitive."
        ),
    )


class ImageUpdateSchema(BaseModel):
    url: HttpUrl = Field(MISSING, description=IMAGE_URL_DESCRIPTION)

    rating: Rating = Field(MISSING, description=IMAGE_RATING_DESCRIPTION)

    source_id: str | None = Field(MISSING, description=IMAGE_SOURCE_ID_DESCRIPTION)
    source_url: HttpUrl | None = Field(MISSING, description=IMAGE_SOURCE_URL_DESCRIPTION)

    artist_name: str | None = Field(MISSING, description=IMAGE_ARTIST_NAME_DESCRIPTION)

    tags: list[NanoID | str] = Field(
        MISSING,
        description=(
            "A list of tags to associate with this image. Each item can be a tag ID or a tag "
            "name. Tag names are case-insensitive."
        ),
    )


TAG_NAME_DESCRIPTION = "The name of this tag."
TAG_IS_NSFW_DESCRIPTION = "Whether this tag is considered NSFW (Not Safe For Work)."


class TagReadSchema(BaseModel):
    id: NanoID = Field(..., description="The unique identifier of this tag.")

    name: str = Field(..., description=TAG_NAME_DESCRIPTION)
    is_nsfw: bool = Field(..., description=TAG_IS_NSFW_DESCRIPTION)

    created_at: datetime = Field(
        ...,
        description="The date and time this tag was added to the database.",
    )
    updated_at: datetime = Field(
        ...,
        description="The date and time this tag was last updated in the database.",
    )

    @classmethod
    def from_orm(cls, obj: Tag) -> "TagReadSchema":
        return cls(
            id=obj.id,
            name=obj.name,
            is_nsfw=obj.is_nsfw,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )


class TagCreateSchema(BaseModel):
    name: str = Field(..., description=TAG_NAME_DESCRIPTION)
    is_nsfw: bool = Field(..., description=TAG_IS_NSFW_DESCRIPTION)


class TagUpdateSchema(BaseModel):
    name: str = Field(MISSING, description=TAG_NAME_DESCRIPTION)
    is_nsfw: bool = Field(MISSING, description=TAG_IS_NSFW_DESCRIPTION)
