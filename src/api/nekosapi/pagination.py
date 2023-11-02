from typing import Any

from django.db.models import QuerySet

from ninja import Schema, Field
from ninja.conf import settings
from ninja.pagination import PaginationBase


class LimitOffsetPagination(PaginationBase):
    class Input(Schema):
        limit: int = Field(
            settings.PAGINATION_PER_PAGE, ge=1, le=settings.PAGINATION_PER_PAGE
        )
        offset: int = Field(0, ge=0)

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Input,
        **params: Any,
    ) -> Any:
        offset = pagination.offset
        limit: int = pagination.limit
        return {
            "items": queryset[offset : offset + limit],
            "count": self._items_count(queryset),
        }  # noqa: E203


class LimitPagination(PaginationBase):
    class Input(Schema):
        limit: int = Field(
            settings.PAGINATION_PER_PAGE, ge=1, le=settings.PAGINATION_PER_PAGE
        )

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Input,
        **params: Any,
    ) -> Any:
        limit: int = pagination.limit
        return {
            "items": queryset[:limit],
            "count": self._items_count(queryset),
        }  # noqa: E203
