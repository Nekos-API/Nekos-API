from tortoise import Tortoise
from tortoise.migrations import api as migrations

from nekos_api.lib import settings


async def on_startup():
    """Connects to the database and creates the missing schemas on FastAPI startup."""

    await migrations.migrate(config=settings.DATABASE)
    await Tortoise.init(config=settings.DATABASE, _enable_global_fallback=True)


async def on_shutdown():
    """Closes the database connections on FastAPI shutdown."""

    await Tortoise.close_connections()
