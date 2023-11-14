from django.shortcuts import get_object_or_404

from ninja import Router, Query
from ninja.pagination import paginate

from nekosapi.utils import async_get_or_404
from nekosapi.pagination import LimitOffsetPagination
from nekosapi.images.schemas import ImageSchema
from nekosapi.artists.models import Artist
from nekosapi.artists.schemas import ArtistSchema
from nekosapi.artists.filters import ArtistFilterSchema


router = Router(tags=["Artists"])


@router.get(
    "",
    response={200: list[ArtistSchema]},
    summary="Get all artists",
    description="Returns a paginated list of all artists listed in the API.",
)
@paginate(LimitOffsetPagination)
def artists(request, filters: ArtistFilterSchema = Query(...)):
    return filters.filter(Artist.objects.all())


@router.get(
    "/{id}",
    response={200: ArtistSchema},
    summary="Get an artist by ID",
    description="Returns a single artist by it's ID. You'll get a 404 if the artist doesn't exist.",
)
async def artist(request, id: int):
    return await async_get_or_404(Artist, id=id)


@router.get(
    "/{id}/images",
    response={200: list[ImageSchema]},
    summary="Get an artist's images",
    description="Returns a paginated list of an artist's images.",
)
@paginate(LimitOffsetPagination)
def artist_images(request, id: int):
    return get_object_or_404(
        Artist.objects.prefetch_related("images"), id=id
    ).images.all()
