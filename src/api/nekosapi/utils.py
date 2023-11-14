import os

from django.db.models import Model
from django.db.models.base import ModelBase
from django.core.exceptions import ObjectDoesNotExist

from nekosapi.errors import HttpError


def getsecret(name: str, default=None, env_fallback: bool = True):
    """Returns a Docker secret's value.

    Args:
        name (str): The name of the secret.
        default (_type_, optional): The default value in case the secret doesn't exist. Defaults to None.
        env_fallback (bool, optional): Whether to fallback to the environment variable if the secret doesn't exist. Defaults to True.
    """

    try:
        with open("/run/secrets/" + name) as f:
            return f.read()
    except FileNotFoundError:
        return os.getenv(name, default) if env_fallback else default


async def async_get_or_404(
    qs,
    **kwargs,
) -> Model:
    print(isinstance(qs, Model), type(qs))

    if isinstance(qs, ModelBase):
        qs = qs.objects

    try:
        return await qs.aget(**kwargs)
    except ObjectDoesNotExist:
        raise HttpError(
            404,
            [
                {
                    "loc": list(kwargs.keys()),
                    "msg": f"Could not find {qs.model.__name__.title()} with {', '.join(f'{k}={v}' for k, v in kwargs.items())}",
                    "type": "not_found",
                    "ctx": {
                        "id": kwargs["id"],
                    }
                    if "id" in kwargs
                    else {},
                }
            ],
        )
