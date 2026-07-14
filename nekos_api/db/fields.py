import nanoid

from tortoise import fields


def NanoIDField(*args, **kwargs):
    """A nanoid DB field.

    This is an alias for a CharField with a max length of 21 characters, using
    `nanoid.generate` as the default value generator. The arguments and keyword
    arguments are passed directly to the CharField constructor.

    Arguments:
        *args: Positional arguments for the CharField.
        **kwargs: Keyword arguments for the CharField.

    Returns:
        tortoise.fields.CharField: A CharField configured as a nanoid primary key.
    """

    return fields.CharField(
        max_length=21,
        default=nanoid.generate,
        *args,
        **kwargs,
    )
