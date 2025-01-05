import json

from django.core.files.base import ContentFile

import requests

from nekosapi.images.models import Image


images = json.load(open("images.json", encoding="UTF-8"))
i = 0

loaded_ids = Image.objects.values_list("id", flat=True)


for image in images:
    if image["id"] in loaded_ids:
        print(f"Image {image['id']} already exists in the database", end="\r")
        continue

    r = None

    while True:
        try:
            r = requests.get(image["url"])
            break

        except requests.exceptions.RequestException:
            print(f"Failed to download {image['url']}. Retrying...", end="\r")

    if r.status_code != 200:
        print(f"Failed to download {image['url']}")
        continue

    while True:
        try:
            img = Image.objects.create(
                id=image["id"],
                file=ContentFile(r.content, name=image["url"].split("/")[-1]),
                rating=image["rating"],
                color_dominant=image["color"]["dominant"],
                color_palette=image["color"]["palette"],
                artist_name=image["artist"],
                tags=[tag.replace(" ", "_").lower() for tag in image["tags"]],
                source_name=image["source"]["name"],
                source_id=image["source"]["id"],
            )

            break

        except Exception as e:
            print(f"Failed to create image {image['id']}. Retrying...", end="\r")

    i += 1
    print(f"Imported {i} images. Last image URL: {image["url"]}", end="\r")
