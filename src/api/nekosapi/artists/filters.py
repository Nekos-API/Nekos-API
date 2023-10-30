from typing import Optional

from ninja import FilterSchema, Field


class ArtistFilterSchema(FilterSchema):
    search: Optional[str] = Field(
        None,
        q=["name__icontains", "aliases__icontains"],
        expression_operator="OR",
        description="Search term. Will return all tags with this term(s) in their name or description."
    )
    policy_repost: Optional[bool] = Field(
        None,
        title="Reposting",
        description="Does this artist allow you to repost their art in other places?",
    )
    policy_credit: Optional[bool] = Field(
        None,
        title="Crediting",
        description="Are you required to credit the artist when using their art?",
    )
    policy_ai: Optional[bool] = Field(
        None,
        title="AI Training",
        description="Does the artist allow you to use their art for AI projects (AI training)?",
    )
