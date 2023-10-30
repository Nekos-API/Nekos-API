from typing import Optional

from ninja import Schema, Field


class ArtistSchema(Schema):
    id: int = Field(..., title="ID", description="The artist's ID.")
    id_v2: Optional[str] = Field(
        ..., title="ID v2", description="The artist's ID in the v2 API. Format: UUID"
    )

    name: str = Field(..., description="The artist's name.")
    aliases: list[str] = Field(
        ...,
        title="Aliases (AKA)",
        description="Other names by which the artist is known.",
    )

    image_url: Optional[str] = Field(
        ...,
        alias="image",
        title="PFP",
        description="An attempt to serve an artist PFP. This will probably stay outdated if they change their image after we upload it (they probably will at some point).",
    )

    links: list[str] = Field(
        ...,
        description="A list of links to official pages for the artist, like SNS or their website. They may be outdated if the artist changes their URL.",
    )

    policy_repost: Optional[bool] = Field(
        ...,
        title="Reposting",
        description="Does this artist allow you to repost their art in other places?",
    )
    policy_credit: bool = Field(
        True,
        title="Crediting",
        description="Are you required to credit the artist when using their art?",
    )
    policy_ai: bool = Field(
        False,
        title="AI Training",
        description="Does the artist allow you to use their art for AI projects (AI training)?",
    )
