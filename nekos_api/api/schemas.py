from typing import Annotated

import nanoid

from fastapi import Query

from pydantic import BaseModel, Field

from tortoise.queryset import QuerySet


NanoID = Annotated[
    str,
    Field(
        min_length=21,
        max_length=21,
        pattern="^[A-Za-z0-9_-]{21}$",
        example=nanoid.generate(),
    ),
]
"""A nanoid identifier type for pydantic models.

Example:
```
from pydantic import BaseModel

from project.api.schemas import NanoID


class BookSchema(BaseModel):
    id: NanoID
    title: str
```
"""


class ErrorSchema(BaseModel):
    """A standard error response schema."""

    title: str = Field(..., description="A short title for this error.")
    message: str = Field(..., description="A detailed message describing this error.")


class Page[T](BaseModel):
    """A standard paginated response schema."""

    items: list[T] = Field(..., description="The list of items on this page.")
    total: int = Field(..., description="The total number of items available across all pages.")

    @classmethod
    async def from_queryset(
        cls, schema: type[BaseModel], qs: QuerySet, params: "PageParams"
    ) -> "Page[T]":
        """Creates a paginated response from a Tortoise ORM QuerySet.

        Args:
            schema (type[Schema]): The schema type to serialize items with.
            qs (QuerySet): The Tortoise ORM QuerySet to paginate.
            params (PageParams): The pagination parameters.

        Returns:
            Page[T]: A paginated response containing serialized items.
        """

        total = await qs.count()
        items = await qs.limit(params.limit).offset(params.offset)

        return cls(items=[schema.from_orm(item) for item in items], total=total)


class _PageParams(BaseModel):
    """The standard pagination query parameters."""

    limit: int = Field(
        25, le=100, description="The maximum number of items to return in the response."
    )
    offset: int = Field(
        0,
        ge=0,
        description="The number of items to skip before starting to collect the result set.",
    )


PageParams = Annotated[_PageParams, Query()]
"""The standard pagination query parameters annotation.

It wraps a `_PageParams` model for use in FastAPI route definitions without requiring
`Annotated[PageParams, Query()]` on every use.
"""
