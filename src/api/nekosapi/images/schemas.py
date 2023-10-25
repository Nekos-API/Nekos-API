from typing import List, Optional

from ninja import Schema, Field

from nekosapi.images.models import Image, Tag
from nekosapi.artists.schemas import ArtistSchema
from nekosapi.characters.schemas import CharacterSchema


class ImageSchema(Schema):
    id: int = Field(..., title="ID", description="The image's ID.")

    image_url: str = Field(
        ...,
        alias="image",
        title="Image URL",
        description="The original/full image's URL. The format is always WEBP.",
    )
    sample_url: str = Field(
        ...,
        alias="sample",
        title="Sample URL",
        description="The sample image's URL. It's a reduced version of the original image that is either 360px tall or 360px wide, whichever is smaller. The format is always WEBP.",
    )

    image_size: int = Field(
        ..., title="Image Size", description="The file size of the image."
    )
    image_width: int = Field(
        ..., title="Image Width", description="The width of the image."
    )
    image_height: int = Field(
        ..., title="Image Height", description="The height of the image."
    )
    sample_size: int = Field(
        ..., title="Sample Size", description="The file size of the sample image."
    )
    sample_width: int = Field(
        ..., title="Sample Width", description="The width of the sample image."
    )
    sample_height: int = Field(
        ..., title="Sample Height", description="The height of the sample image."
    )

    source: Optional[str] = Field(
        ...,
        title="Source",
        description="The source URL of the image (where it was first posted).",
    )
    source_id: Optional[int] = Field(
        ...,
        title="Source ID",
        description="The source ID of the sauce in [NekoSauce](https://nekosauce.org).",
    )

    rating: str = Field(
        ...,
        title="Rating",
        description="The age rating of the image.",
    )
    verification: str = Field(
        ...,
        title="Verification",
        description="The verification level of the image. Normal users will only see images with this set to `verified`.",
    )

    hash_md5: Optional[str] = Field(
        ...,
        title="MD5 Hash",
        description="The MD5 hash of the image. This is a(n almost) unique identifier for the image.",
    )
    hash_perceptual: Optional[str] = Field(
        ...,
        title="Perceptual Hash",
        description="The perceptual hash of the image. This can be used to compare this image to other images.",
    )

    color_dominant: Optional[list[int]] = Field(
        ...,
        title="Dominant Color",
        description="The dominant color of the image. [R, G, B]",
    )
    color_palette: Optional[list[list[int]]] = Field(
        ...,
        title="Color Palette",
        description="The color palette of the image. [[R, G, B], [R, G, B], ...]",
    )

    duration: Optional[int] = Field(
        ...,
        title="Duration",
        description="The amount of frames that make up the image (if it's animated, check `is_animated`).",
    )

    is_original: bool = Field(
        ...,
        title="Is Original",
        description="Whether the image's idea is original or it uses characters/settings/content from another place (not original).",
    )
    is_screenshot: bool = Field(
        ...,
        title="Is Screenshot",
        description="Whether the image is a screenshot of an anime ep./manga page.",
    )
    is_flagged: bool = Field(
        ..., title="Is Flagged", description="Whether the image is flagged by mods."
    )
    is_animated: bool = Field(
        ...,
        title="Is Animated",
        description="Whether the image is animated or not. This'll become useful in the future when we add GIFs.",
    )

    artist: Optional[ArtistSchema] = Field(
        ...,
        title="Artist",
        description="The artist of the image.",
    )
    characters: list[CharacterSchema] = Field(
        ...,
        title="Characters",
        description="The characters that appear in the image.",
    )
    tags: list["TagSchema"] = Field(
        ...,
        title="Tags",
        description="The image's tags.",
    )

    created_at: float = Field(
        ...,
        title="Created At",
        description="The time the image was created. This value is a POSIX timestamp.",
    )
    updated_at: float = Field(
        ...,
        title="Updated At",
        description="The time the image was last updated. This value is a POSIX timestamp.",
    )

    @staticmethod
    def resolve_created_at(obj: Image) -> int:
        return obj.created_at.timestamp()

    @staticmethod
    def resolve_updated_at(obj: Image) -> int:
        return obj.updated_at.timestamp()


class TagSchema(Schema):
    id: int = Field(..., title="ID", description="The tag's ID.")

    name: str = Field(..., description="The tag's name.")
    description: str = Field(
        ...,
        description="A short description that says what the tag is and when it applies.",
    )

    is_nsfw: bool = Field(
        ...,
        title="NSFW",
        description="Whether the tag is NSFW or not (usually, tags with this set to true will only be on NSFW images).",
    )


ImageSchema.update_forward_refs()
