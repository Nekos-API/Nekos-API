from datetime import datetime

import io

from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

import orjson

from images.models import Image


class Command(BaseCommand):
    help = "Exports images.json to the CDN's base dir"

    def handle(self, *args, **options):
        self.stdout.write("Exporting `images.json`...")

        payload = orjson.dumps(
            {
                "images": [
                    {
                        "id": image.id,
                        "title": image.title,
                        "is_nsfw": image.age_rating
                        not in [Image.AgeRating.SFW, Image.AgeRating.QUESTIONABLE],
                        "tags": list(image.categories.values_list("id", flat=True)),
                        "charaters": list(
                            image.characters.values_list("id", flat=True)
                        ),
                        "artist": image.artist_id,
                    }
                    for image in Image.objects.filter(
                        verification_status=Image.VerificationStatus.VERIFIED
                    ).prefetch_related("categories", "characters")
                ],
                "meta": {
                    "count": Image.objects.count(),
                    "updated": datetime.utcnow().isoformat(),
                },
            }
        )

        default_storage.save("images.json", io.BytesIO(payload.encode()))

        self.stdout.write("Done! `images.json` has been saved.")
