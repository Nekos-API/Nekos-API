import os

from django.db.models import Model

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
    model: Model,
    prefetch_related: list[str] = [],
    select_related: list[str] = [],
    **kwargs,
) -> Model:
    qs = model.objects.prefetch_related(*prefetch_related).select_related(
        *select_related
    )
    try:
        return await qs.aget(**kwargs)
    except model.DoesNotExist:
        raise HttpError(
            404,
            [
                {
                    "loc": list(kwargs.keys()),
                    "msg": f"Could not find {model.__name__.title()} with {', '.join(f'{k}={v}' for k, v in kwargs.items())}",
                    "type": "not_found",
                    "ctx": {
                        "id": kwargs["id"],
                    }
                    if "id" in kwargs
                    else {},
                }
            ],
        )
