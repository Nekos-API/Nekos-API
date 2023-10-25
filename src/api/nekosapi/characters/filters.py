from typing import Optional

from ninja import Field, FilterSchema


class CharacterFilterSchema(FilterSchema):
    search: Optional[str] = Field(
        None,
        q=["name__icontains", "aliases__icontains", "description__icontains"],
        expression_operator="OR",
    )
    gender: Optional[str] = Field(
        None,
        title="Gender",
        description="The character's gender.",
        q="gender__iexact",
    )
    species: Optional[str] = Field(
        None,
        title="Species",
        description="The character's species.",
        q="species__iexact",
    )
    nationality: Optional[str] = Field(
        None,
        title="Nationality",
        description="The character's nationality.",
        q="nationality__iexact",
    )
    occupations: Optional[list[str]] = Field(
        None,
        title="Occupations",
        description="Occupations the character officially has/has officially had.",
        q="occupations__in",
    )
