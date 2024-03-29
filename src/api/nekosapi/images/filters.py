from typing import Optional, Union

from django.db.models import Q

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
    artist: Optional[int] = Field(None, title="Artist", description="The artist's ID.")
    character: Optional[list[int]] = Field(
        None,
        title="Character(s)",
        description="The character's ID.",
    )
    tag: Optional[list[int]] = Field(
        None,
        title="Tag(s)",
        description="The tag's ID.",
    )

    def filter_tag(self, value: list[int] | None) -> Q:
        if value is None: return Q()

        q = Q()

        for tag_id in value:
            q |= Q(tags__id=tag_id)

        return q

    def filter_character(self, value: list[int] | None) -> Q:
        if value is None: return Q()

        q = Q()

        for character_id in value:
            q |= Q(characters__id=character_id)

        return q


class TagFilterSchema(FilterSchema):
    search: Optional[str] = Field(
        None,
        q=["name__icontains", "description__icontains"],
        expression_operator="OR",
        description="Search for a tag by name or description.",
    )
    is_nsfw: Optional[bool] = Field(
        None, title="Is NSFW", description="Whether the tag is NSFW or not."
    )
