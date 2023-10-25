from typing import Optional, Union

from ninja import Field, FilterSchema

from nekosapi.images.models import Image


class ImageFilterSchema(FilterSchema):
    rating: Optional[list[str]] = Field(
        None,
        title="Age Rating",
        description="The age rating of the image.",
        q="rating__in",
    )
    is_original: Optional[bool] = Field(
        None,
        title="Is Original",
        description="Whether the image's idea is original or it uses characters/settings/content from another place (not original).",
    )
    is_screenshot: Optional[bool] = Field(
        None,
        title="Is Screenshot",
        description="Whether the image is a screenshot of an anime ep./manga page.",
    )
    is_flagged: Optional[bool] = Field(
        None, title="Is Flagged", description="Whether the image is flagged by mods."
    )
    is_animated: Optional[bool] = Field(
        None,
        title="Is Animated",
        description="Whether the image is animated or not. This'll become useful in the future when we add GIFs.",
    )
    artist: Optional[list[int]] = Field(
        None,
        title="Artist(s)",
        description="The artist's ID. Can be set multiple times (in the same query) to filter by multiple artists.",
        q="artist__id__in",
    )
    character: Optional[list[int]] = Field(
        None,
        title="Character(s)",
        description="The character's ID. Can be set multiple times (in the same query) to filter by multiple characters.",
        q="character__id__in",
    )
    tag: Optional[list[int]] = Field(
        None,
        title="Tag(s)",
        description="The tag's ID. Can be set multiple times (in the same query) to filter by multiple tags.",
        q="tag__id__in",
    )


class TagFilterSchema(FilterSchema):
    search: Optional[str] = Field(
        None,
        q=["name__icontains", "description__icontains"],
        expression_operator="OR",
    )
    is_nsfw: Optional[bool] = Field(
        None, title="Is NSFW", description="Whether the tag is NSFW or not."
    )
