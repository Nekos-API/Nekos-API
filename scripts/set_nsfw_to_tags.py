import asyncio

from nekos_api.db import Tag, lifespan as db


async def main():
    print("Starting database connections...")
    await db.on_startup()

    tags = await Tag.all()
    print(f"Found {len(tags)} tags in the database.")

    for tag in tags:
        is_nsfw = input(f"Is the tag '{tag.name}' NSFW? (y/n): ").strip().lower() == "y"
        tag.is_nsfw = is_nsfw

    print(f"Updating {len(tags)} tags in the database...")
    await Tag.bulk_update(tags, fields=["is_nsfw"])

    print("Shutting down database connections...")
    await db.on_shutdown()


asyncio.run(main())
