from ninja import schema

from . import models


class ImageSchema(schema.Schema):
    id: int
    url: str = schema.Field(alias="file")
    rating: models.Image.Rating
    color_dominant: tuple[int, int, int]
    color_palette: list[tuple[int, int, int]]
    artist_name: str | None
    tags: list[str]
    source_url: str | None = schema.Field(alias="source_name")
