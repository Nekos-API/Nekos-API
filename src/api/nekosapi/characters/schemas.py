from uuid import UUID
from typing import Optional

from ninja import Schema, Field

from nekosapi.characters.models import Character


class CharacterSchema(Schema):
    id: int = Field(..., title="ID", description="The character's ID.")
    id_v2: Optional[UUID] = Field(
        ..., title="ID v2", description="The character's ID in the v2 API. Format: UUID"
    )

    name: str = Field(..., description="The character's name.")
    aliases: list[str] = Field(
        ...,
        title="Aliases (AKA)",
        description="Other names by which the character is known.",
    )

    description: Optional[str] = Field(
        ...,
        title="Description",
        description="A description of the character.",
    )

    ages: list[int] = Field(
        ...,
        title="Ages",
        description="All the ages the character officially has/has officially had.",
    )
    height: Optional[int] = Field(
        ...,
        title="Height",
        description="The the character's height (in cm).",
    )
    weight: Optional[int] = Field(
        ...,
        title="Weight",
        description="The character's weight (in kg).",
    )
    gender: Optional[str] = Field(
        ...,
        description="The character's gender.",
    )
    species: Optional[str] = Field(
        ...,
        description="The character's species.",
    )
    birthday: Optional[str] = Field(
        ...,
        description="The character's birthday. Format: MM/DD",
    )
    nationality: Optional[str] = Field(
        ...,
        description="The character's nationality.",
    )
    occupations: Optional[list[str]] = Field(
        ...,
        description="All the occupations the character officially has/has officially had.",
    )

    @staticmethod
    def resolve_birthday(obj: Character) -> Optional[str]:
        return obj.birthday.strftime("%m/%d") if obj.birthday else None
