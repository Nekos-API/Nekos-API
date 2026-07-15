import asyncio

from typing import TypedDict

import orjson

from nekos_api.db import lifespan as db, Image
from nekos_api.lib.requests import httpx


class ImageV4(TypedDict):
    id: int
    url: str


async def get_images(page: int) -> list[ImageV4]:
    response = await httpx.get(f"https://api.nekosapi.com/v4/images?limit=100&offset={(page - 1) * 100}")

    return response.json()["items"]

async def main():
    print("Starting database connections...")
    await db.on_startup()

    print("Reading images.json file...")
    json: list[ImageV4] = orjson.loads(open("images.json", "rb").read())
    json_dict = {image["id"]: image for image in json}

    page = 1

    while True:
        print(f"Fetching page {page}...")
        images = await get_images(page)

        if not images:
            break

        to_update = []

        for image in images:
            new_url = image["url"]
            old_url = json_dict[image["id"]]["url"]

            row = await Image.get_or_none(url=old_url)

            if row is None:
                print(f"Image with URL {old_url} not found in the database.")
                continue

            row.url = new_url
            to_update.append(row)

        if to_update:
            print(f"Updating {len(to_update)} images in the database...")
            await Image.bulk_update(to_update, fields=["url"])

        page += 1

    print("Shutting down database connections...")
    await db.on_shutdown()


asyncio.run(main())
