from typing import Annotated

from fastapi import Depends, Header

from nekos_api.lib import settings
from nekos_api.api.errors import UnauthorizedError, ValidationError


async def _authenticate(
    authorization: Annotated[
        str,
        Header(
            ...,
            description="The administration token, used to authorize administrator-only operations.",
        ),
    ],
) -> None:
    """Validates the Authorization header for admin-only endpoints."""

    parts = authorization.split(" ")

    if not len(parts) == 2 or parts[0].lower() != "bearer":
        raise ValidationError(
            title="Invalid Authorization Header",
            message="Authorization header must be in the format 'Bearer <token>'.",
        )

    token = parts[1]

    if not settings.ADMIN_TOKEN or token != settings.ADMIN_TOKEN:
        raise UnauthorizedError(
            "The token you provided in the Authorization header is invalid."
        )

    return None


AdminAuth = Annotated[None, Depends(_authenticate)]
"""Requires the Authorization header to be set to the admin token.

Raises:
    ValidationError: If the Authorization header is not in the correct format.
    UnauthorizedError: If the Authorization header is not set or the token is invalid.

Returns:
    None: If the Authorization header is valid and the token is correct.
"""
