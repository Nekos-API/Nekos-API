import os
import time

from django.core.management.base import BaseCommand, CommandError

import requests

from images.models import Image, ImageSourceResult


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Handle image source fetching.
        """

        for image in Image.objects.filter(source_queries=None)[:100]:
            # Handle the 100 daily images.

            file_url = image.file.url

            with requests.get(file_url) as f:
                r = requests.post(
                    "https://saucenao.com/search.php",
                    params={
                        "db": 999,
                        "output_type": 2,
                        "testmode": 1,
                        "numres": 8,
                        "api_key": os.getenv("SAUCENAO_TOKEN"),
                    },
                    files=dict(file=f.content),
                )

                res = ImageSourceResult.objects.create(
                    image=image,
                    result=r.json(),
                    source=ImageSourceResult.Sources.SAUCE_NAO,
                    status=r.status_code
                )

                self.stdout.write(
                    f"QUERIED - Image ID: {image.id} - Status code: {r.status_code}"
                )
                self.stdout.write("Sleeping 10s...\n")
                time.sleep(10)
