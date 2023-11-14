from django.shortcuts import get_object_or_404

from ninja import Schema, Router, Query
from ninja.pagination import paginate

from nekosapi.utils import async_get_or_404
from nekosapi.pagination import LimitOffsetPagination
from nekosapi.images.schemas import ImageSchema
from nekosapi.characters.models import Character
from nekosapi.characters.schemas import CharacterSchema
from nekosapi.characters.filters import CharacterFilterSchema


router = Router(tags=["Characters"])


@router.get(
    "",
    response={200: list[CharacterSchema]},
    summary="Get all characters",
    description="Returns a paginated list of all characters in the API.",
)
@paginate(LimitOffsetPagination)
def characters(request, filters: CharacterFilterSchema = Query(...)):
    return filters.filter(Character.objects.all())


@router.get(
    "/{id}",
    response={200: CharacterSchema},
    summary="Get a character by ID",
    description="Returns a character by it's ID. You'll get a 404 if the character doesn't exist.",
)
async def character(request, id: int):
    return await async_get_or_404(Character, id=id)


@router.get(
    "/{id}/images",
    response={200: list[ImageSchema]},
    summary="Get a character's images",
    description="Returns a paginated list of a character's images.",
)
@paginate(LimitOffsetPagination)
def character_images(request, id: int):
    return get_object_or_404(
        Character.objects.prefetch_related("images"), id=id
    ).images.all()
