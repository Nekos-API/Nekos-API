import secrets

from django.http import Http404
from django.shortcuts import redirect

from ninja import Router, Query
from ninja.pagination import paginate

from nekosapi.utils import async_get_or_404
from nekosapi.pagination import LimitOffsetPagination, LimitPagination
from nekosapi.images.models import Image, Tag
from nekosapi.images.schemas import ImageSchema, TagSchema
from nekosapi.images.filters import ImageFilterSchema, TagFilterSchema


router = Router(tags=["Images"])


@router.get(
    "",
    response={200: list[ImageSchema]},
    summary="Get all images",
    description="Returns a paginated list of all the verified images in the API.",
)
@paginate(LimitOffsetPagination)
def images(request, filters: ImageFilterSchema = Query(...)):
    qs = (
        Image.objects.prefetch_related("tags", "characters")
        .select_related("artist")
        .filter(verification=Image.Verification.VERIFIED)
    )
    qs = filters.filter(qs)
    return qs


@router.get(
    "/random",
    response={200: list[ImageSchema]},
    summary="Get random images",
    description="Returns x random images. It supports all the same filters than the /images endpoint.",
)
@paginate(LimitPagination)
def random_images(request, filters: ImageFilterSchema = Query(...)):
    qs = (
        Image.objects.filter(verification=Image.Verification.VERIFIED)
        .prefetch_related("tags", "characters")
        .select_related("artist")
    )
    qs = filters.filter(qs)
    return qs.order_by("?")


@router.get(
    "/random/file",
    summary="Get a random image file redirect",
    description="Redirects to a random image file URL.",
)
def random_image_file(request, filters: ImageFilterSchema = Query(...)):
    qs = Image.objects.filter(verification=Image.Verification.VERIFIED)
    qs = filters.filter(qs)
    image = secrets.choice(qs)
    return redirect(image.image.url)


@router.get(
    "/tags",
    response={200: list[TagSchema]},
    summary="Get all tags",
    description="Returns a list of all tags in the API. You can use this endpoint to create filters in your app.",
)
@paginate(LimitOffsetPagination)
def tags(request, filters: TagFilterSchema = Query(...)):
    return filters.filter(Tag.objects.all())


@router.get(
    "/tags/{id}",
    response={200: TagSchema},
    summary="Get a tag by ID",
    description="Returns a tag by it's ID. You'll get a 404 if the tag doesn't exist.",
)
async def tag(request, id: int):
    return await async_get_or_404(Tag, id=id)


@router.get(
    "/{id}",
    response={200: ImageSchema},
    summary="Get an image by ID",
    description="Returns an image by it's ID. You'll get a 404 if the image doesn't exist. (This endpoint is here below because all the previous ones are resolved first).",
)
async def image(request, id: int):
    return await async_get_or_404(
        Image,
        prefetch_related=["tags", "characters"],
        select_related=["artist"],
        id=id,
        verification=Image.Verification.VERIFIED,
    )
