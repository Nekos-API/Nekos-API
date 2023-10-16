import os
import random


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
