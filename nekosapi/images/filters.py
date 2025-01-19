from typing import Annotated, TypeVar

from django.db.models import Q

import ninja

import pydantic

from . import models


T = TypeVar("T")


CommaList = Annotated[
    list[T],
    pydantic.BeforeValidator(
        lambda x: [v for v in (v.strip() for v in x.split(",")) if v]
    ),
]


class ImageFilters(ninja.FilterSchema):
    tags: CommaList[str] | None = ninja.Field(None, q="tags__contains")
    without_tags: CommaList[str] | None = None
    rating: CommaList[models.Image.Rating] | None = ninja.Field(
        None,
        q="rating__in",
    )
    artist_name: str | None = None

    def filter_without_tags(self, value: CommaList[str]) -> Q:
        return ~Q(tags__overlap=value) if value else Q()
