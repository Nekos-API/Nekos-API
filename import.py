import asyncio

from typing import TypedDict

import orjson

from nekos_api.db import Image, Tag, Rating, lifespan as db


class ImageSchema(TypedDict):
    id: int
    url: str
    rating: str
    color: "ImageColorSchema"
    artist: str | None
    source: "ImageSourceSchema"


class ImageColorSchema(TypedDict):
    dominant: tuple[int, int, int]
    palette: list[tuple[int, int, int]]


class ImageSourceSchema(TypedDict):
    id: str | None
    name: str | None


async def main():
    print("Starting database connections...")
    await db.on_startup()

    # A map of the name of each tag to its row in the database.
    tags: dict[str, Tag] = {}

    print("Reading images.json file...")

    f = open("images.json", "rb")
    images: list[ImageSchema] = orjson.loads(f.read())
    f.close()

    print(f"Importing {len(images)} images into the database...")

    for image in images:
        for tag_name in image["tags"]:
            if tag_name not in tags:
                tags[tag_name] = await Tag.create(name=tag_name)

    print(f"  Created {len(tags)} tags in the database.")

    for image in images:
        row = await Image.create(
            url=image["url"],
            rating=Rating(image["rating"]),
            color_primary="#%02x%02x%02x" % tuple(image["color"]["dominant"]),
            color_palette=",".join(
                "#%02x%02x%02x" % tuple(c) for c in image["color"]["palette"]
            ),
            artist_name=image["artist"],
            source_id=image["source"]["id"],
            source_url=image["source"]["name"],
        )

        await row.tags.add(*[tags[tag_name] for tag_name in image["tags"]])

    print(f"  Created {len(images)} images in the database.")
    print("Shutting down database connections...")

    await db.on_shutdown()



if __name__ == "__main__":
    asyncio.run(main())
