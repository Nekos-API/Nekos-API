from fastapi import FastAPI

from contextlib import asynccontextmanager

from nekos_api.db import lifespan as db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.on_startup()

    yield

    await db.on_shutdown()
