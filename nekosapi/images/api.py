from typing import Annotated

from django.http import response

import ninja
import ninja.pagination
import ninja.responses

from . import models, schemas, filters


router = ninja.Router()


@router.get("/images", response=list[schemas.ImageSchema])
@ninja.pagination.paginate(ninja.pagination.LimitOffsetPagination)
def get_images(
    request, image_filters: filters.ImageFilters = ninja.Query(...)
) -> list[schemas.ImageSchema]:
    return models.Image.objects.filter(image_filters.get_filter_expression())


@router.get("/images/random", response=list[schemas.ImageSchema])
def get_random_images(
    request,
    limit: Annotated[int, ninja.Field(default=10, ge=1, le=100)],
    image_filters: filters.ImageFilters = ninja.Query(...),
) -> list[schemas.ImageSchema]:
    return models.Image.objects.filter(image_filters.get_filter_expression()).order_by(
        "?"
    )[:limit]


@router.get("/images/random/file")
async def get_random_image_file(
    request, image_filters: filters.ImageFilters = ninja.Query(...)
):
    # Returns a redirect to a random image's URL.

    image = (
        models.Image.objects.filter(image_filters.get_filter_expression())
        .order_by("?")
        .first()
    )

    return response.HttpResponseRedirect(image.file.url)


@router.get("/images/{image_id}", response=schemas.ImageSchema)
async def get_image(request, image_id: int) -> schemas.ImageSchema:
    return await models.Image.objects.aget(id=image_id)


@router.get("/images/{image_id}/file")
async def get_image_file(request, image_id: int):
    # Returns a redirect to the file's URL.

    image = await models.Image.objects.aget(id=image_id)

    return response.HttpResponseRedirect(image.file.url)
