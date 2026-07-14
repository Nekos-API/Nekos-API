import secrets

from io import BytesIO

from typing import Annotated

from fastapi import APIRouter, Query, Path, Response

from pydantic import BaseModel, Field
from pydantic_core import MISSING

from tortoise import transactions
from tortoise.queryset import QuerySet
from tortoise.expressions import Q

from colorthief import ColorThief

from nekos_api.db import Image, Tag, Rating
from nekos_api.lib.requests import httpx
from nekos_api.api.auth import AdminAuth
from nekos_api.api.errors import NotFoundError, FailedDependencyError
from nekos_api.api.schemas import ErrorSchema, PageParams, Page, NanoID
from nekos_api.api.images.schemas import (
    ImageReadSchema,
    ImageCreateSchema,
    ImageUpdateSchema,
    TagReadSchema,
    TagCreateSchema,
    TagUpdateSchema,
)


router = APIRouter(tags=["Images"])


class ImageFilters(BaseModel):
    """Filters for querying images."""

    rating: set[Rating] = Field(
        default_factory=set,
        description="Only return images with rating in the list.",
    )
    artist: set[str] = Field(
        default_factory=set,
        description="Only return images with an artist name in the list.",
        max_length=5,
    )
    tag: set[str] = Field(
        default_factory=set,
        description="Only return images with a tag name or ID in the list.",
        max_length=5,
    )

    def apply(self, queryset: QuerySet[Image]) -> QuerySet[Image]:
        """Apply the filters to the given queryset.

        Args:
            queryset (QuerySet[Image]): The queryset to apply the filters to.

        Returns:
            QuerySet[Image]: The filtered queryset.
        """

        if self.rating:
            queryset = queryset.filter(rating__in=self.rating)

        if self.artist:
            qs = Q()

            for artist in self.artist:
                qs |= Q(artist_name__iexact=artist)

            queryset = queryset.filter(qs)

        if self.tag:
            qs = Q()

            for tag in self.tag:
                qs |= Q(tags__name__iexact=tag) | Q(tags__id=tag)

            queryset = queryset.filter(qs)

        return queryset


class ImageFiltersAndPagination(ImageFilters, PageParams):
    """Filters for querying images with pagination."""


@router.get(
    "/images",
    responses={
        422: {"model": ErrorSchema},
        429: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
)
async def list_images(
    filters: Annotated[ImageFiltersAndPagination, Query()],
) -> Page[ImageReadSchema]:
    """Returns a paginated list of images, filtered by the given parameters.

    The results are ordered by creation date, with the most recent images first.
    """

    queryset = Image.all().prefetch_related("tags").order_by("created_at")
    queryset = filters.apply(queryset)

    return await Page.from_queryset(ImageReadSchema, queryset, filters)


@router.post(
    "/images",
    responses={
        401: {"model": ErrorSchema},
        422: {"model": ErrorSchema},
        429: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
)
@transactions.atomic()
async def create_image(_admin: AdminAuth, image: ImageCreateSchema) -> ImageReadSchema:
    """Creates a new image."""

    tags = await Tag.filter(
        Q(id__in=[tag for tag in image.tags]) | Q(name__in=[tag for tag in image.tags])
    )

    if tags and len(tags) != len(image.tags):
        raise NotFoundError("tag")

    response = await httpx.get(image.url)

    if not response.is_success:
        raise FailedDependencyError(
            "The image URL provided was not reachable or returned a non-successful status code."
        )

    cf = ColorThief(BytesIO(response.content))
    color_primary: tuple[int, int, int] = cf.get_color(quality=1)
    color_palette: list[tuple[int, int, int]] = cf.get_palette(10, 1)

    color_primary = f"#{color_primary[0]:02x}{color_primary[1]:02x}{color_primary[2]:02x}"
    color_palette = [f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}" for color in color_palette]

    row = await Image.create(
        url=image.url,
        rating=image.rating,
        color_primary=color_primary,
        color_palette=color_palette,
        source_id=image.source_id,
        source_url=str(image.source_url),
        artist_name=image.artist_name,
    )

    await row.tags.add(*tags)
    await row.fetch_related("tags")

    return ImageReadSchema.from_orm(row)


@router.get(
    "/images/random",
    responses={
        422: {"model": ErrorSchema},
        429: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
)
async def get_random_image(
    filters: Annotated[ImageFilters, Query()],
) -> ImageReadSchema:
    """Returns a random image, filtered by the given parameters."""

    queryset = Image.all()
    queryset = filters.apply(queryset)

    count = await queryset.count()

    if count == 0:
        raise NotFoundError("image")

    index = secrets.randbelow(count)

    image = await queryset.offset(index).first().prefetch_related("tags")

    return ImageReadSchema.from_orm(image)


@router.get(
    "/images/random/file",
    responses={
        422: {"model": ErrorSchema},
        429: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
    status_code=307,
)
async def get_random_image_file(
    response: Response,
    filters: Annotated[ImageFilters, Query()],
):
    """Returns a random image file URL, filtered by the given parameters."""

    queryset = Image.all()
    queryset = filters.apply(queryset)

    count = await queryset.count()

    if count == 0:
        raise NotFoundError("image")

    index = secrets.randbelow(count)

    image = await queryset.offset(index).first()

    response.headers["Location"] = image.url


@router.get(
    "/images/{image_id}",
    responses={
        404: {"model": ErrorSchema},
        422: {"model": ErrorSchema},
        429: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
)
async def get_image(
    image_id: Annotated[NanoID, Path(..., description="The ID of the image to get.")],
) -> ImageReadSchema:
    """Returns the image with the given ID."""

    image = await Image.get_or_none(id=image_id).prefetch_related("tags")

    if not image:
        raise NotFoundError("image")

    return ImageReadSchema.from_orm(image)


@router.patch(
    "/images/{image_id}",
    responses={
        401: {"model": ErrorSchema},
        404: {"model": ErrorSchema},
        422: {"model": ErrorSchema},
        424: {"model": ErrorSchema},
        429: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
)
@transactions.atomic()
async def update_image(
    _admin: AdminAuth,
    image_id: Annotated[NanoID, Path(..., description="The ID of the image to update.")],
    image: ImageUpdateSchema,
) -> ImageReadSchema:
    """Updates the image with the given ID."""

    row = await Image.get_or_none(id=image_id)

    if row is None:
        raise NotFoundError("image")

    if image.tags is not MISSING:
        tags = await Tag.filter(
            Q(id__in=[tag for tag in image.tags]) | Q(name__in=[tag for tag in image.tags])
        )

        if tags and len(tags) != len(image.tags):
            raise NotFoundError("tag")

        await row.tags.clear()
        await row.tags.add(*tags)

        await row.fetch_related("tags")

    if image.url is not MISSING:
        response = await httpx.get(str(image.url))

        if not response.is_success:
            raise FailedDependencyError(
                "The image URL provided was not reachable or returned a non-successful status code."
            )

        cf = ColorThief(BytesIO(response.content))
        color_primary: tuple[int, int, int] = cf.get_color(quality=1)
        color_palette: list[tuple[int, int, int]] = cf.get_palette(10, 1)

        color_primary = f"#{color_primary[0]:02x}{color_primary[1]:02x}{color_primary[2]:02x}"
        color_palette = ",".join(f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}" for color in color_palette)

        row.color_primary = color_primary
        row.color_palette = color_palette

        row.url = str(image.url)

    if image.rating is not MISSING:
        row.rating = image.rating

    if image.artist_name is not MISSING:
        row.artist_name = image.artist_name

    if image.source_id is not MISSING:
        row.source_id = image.source_id

    if image.source_url is not MISSING:
        row.source_url = image.source_url

    await row.save()
    await row.fetch_related("tags")

    return ImageReadSchema.from_orm(row)


@router.delete(
    "/images/{image_id}",
    responses={
        401: {"model": ErrorSchema},
        404: {"model": ErrorSchema},
        422: {"model": ErrorSchema},
        429: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
    status_code=204,
)
async def delete_image(
    _admin: AdminAuth,
    image_id: Annotated[NanoID, Path(..., description="The ID of the image to delete.")],
):
    """Deletes the image with the given ID."""

    row = await Image.get_or_none(id=image_id)

    if row is None:
        raise NotFoundError("image")

    await row.delete()


@router.get(
    "/images/{image_id}/file",
    responses={
        404: {"model": ErrorSchema},
        422: {"model": ErrorSchema},
        429: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
    status_code=307,
)
async def get_image_file(response: Response, image_id: NanoID):
    """Returns the image file URL for the image with the given ID."""

    image = await Image.get_or_none(id=image_id)

    if not image:
        raise NotFoundError("image")

    response.headers["Location"] = image.url


class TagFilters(BaseModel):
    """Filters for querying tags."""

    name: str | None = Field(
        default=None,
        description="Only return tags with a name that contains the given string.",
    )
    is_nsfw: bool | None = Field(
        default=None,
        description="Only return tags that are NSFW or SFW.",
    )

    def apply(self, queryset: QuerySet[Tag]) -> QuerySet[Tag]:
        """Apply the filters to the given queryset.

        Args:
            queryset (QuerySet[Tag]): The queryset to apply the filters to.

        Returns:
            QuerySet[Tag]: The filtered queryset.
        """

        if self.name:
            queryset = queryset.filter(name__icontains=self.name)

        if self.is_nsfw is not None:
            queryset = queryset.filter(is_nsfw=self.is_nsfw)

        return queryset


class TagFiltersAndPagination(TagFilters, PageParams):
    """Filters for querying tags with pagination."""


@router.get(
    "/tags",
    responses={
        422: {"model": ErrorSchema},
        429: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
)
async def list_tags(page: Annotated[TagFiltersAndPagination, Query()]) -> Page[TagReadSchema]:
    """Returns a paginated list of tags, ordered by name."""

    queryset = Tag.all().order_by("name")

    queryset = page.apply(queryset)

    return await Page.from_queryset(TagReadSchema, queryset, page)


@router.post(
    "/tags",
    responses={
        401: {"model": ErrorSchema},
        422: {"model": ErrorSchema},
        429: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
)
@transactions.atomic()
async def create_tag(_admin: AdminAuth, tag: TagCreateSchema) -> TagReadSchema:
    """Creates a new tag."""

    row = await Tag.create(name=tag.name)

    return TagReadSchema.from_orm(row)


@router.get(
    "/tags/{tag_id}",
    responses={
        404: {"model": ErrorSchema},
        422: {"model": ErrorSchema},
        429: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
)
async def get_tag(tag_id: NanoID) -> TagReadSchema:
    """Returns the tag with the given ID."""

    tag = await Tag.get_or_none(id=tag_id)

    if not tag:
        raise NotFoundError("tag")

    return TagReadSchema.from_orm(tag)


@router.patch(
    "/tags/{tag_id}",
    responses={
        401: {"model": ErrorSchema},
        404: {"model": ErrorSchema},
        422: {"model": ErrorSchema},
        429: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
)
@transactions.atomic()
async def update_tag(
    _admin: AdminAuth,
    tag_id: Annotated[NanoID, Path(..., description="The ID of the tag to update.")],
    tag: TagUpdateSchema,
) -> TagReadSchema:
    """Updates the tag with the given ID."""

    row = await Tag.get_or_none(id=tag_id)

    if row is None:
        raise NotFoundError("tag")

    if tag.name is not MISSING:
        row.name = tag.name

    await row.save()

    return TagReadSchema.from_orm(row)


@router.delete(
    "/tags/{tag_id}",
    responses={
        401: {"model": ErrorSchema},
        404: {"model": ErrorSchema},
        422: {"model": ErrorSchema},
        429: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
    status_code=204,
)
async def delete_tag(
    _admin: AdminAuth,
    tag_id: Annotated[NanoID, Path(..., description="The ID of the tag to delete.")],
):
    """Deletes the tag with the given ID."""

    row = await Tag.get_or_none(id=tag_id)

    if row is None:
        raise NotFoundError("tag")

    await row.delete()
