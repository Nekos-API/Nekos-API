import os
import time

from urllib.parse import urlparse

from django.core.management.base import BaseCommand, CommandError

import requests

from images.models import Image, ImageSourceResult


def get_any_value(d: dict, *keys):
    """
    Returns the first valid key's value.
    """

    for key in keys:
        if key in d:
            return d.get(key)
    return None


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Handle image source fetching.
        """

        for image in Image.objects.filter(source_queries=None, verification_status="verified")[:100]:
            # Handle the 100 daily images.

            file_url = image.file.url

            with requests.get(file_url) as f:
                r = requests.post(
                    "https://saucenao.com/search.php",
                    params={
                        "db": 999,
                        "output_type": 2,
                        "testmode": 1,
                        "numres": 16,
                        "api_key": os.getenv("SAUCENAO_TOKEN"),
                    },
                    files=dict(file=f.content),
                )

                results = r.json()["results"]
                possible_sources = []

                for result in results:
                    if float(result["header"]["similarity"]) >= 85:
                        possible_sources.append(
                            {
                                "title": get_any_value(results, "title", "index_name"),
                                "similarity": float(result["header"]["similarity"]),
                                "ext_urls": result["data"].get("ext_urls"),
                                "source": result["data"].get("source"),
                                "artist": {
                                    "name": get_any_value(
                                        result["data"],
                                        "member_name",
                                        "creator",
                                        "author_name",
                                        "artist",
                                    ),
                                    "url": get_any_value(result["data"], "author_url"),
                                },
                            }
                        )

                if len(possible_sources) == 0:
                    self.stderr.write(
                        f"QUERIED: ERROR - Image ID: {image.id} - Status code: {r.status_code}"
                    )
                    self.stdout.write("Sleeping 10s...\n")
                    time.sleep(10)
                    continue

                possible_sources = sorted(
                    possible_sources, key=lambda d: d["similarity"], reverse=True
                )

                source = possible_sources[0]

                ImageSourceResult.objects.create(
                    image=image,
                    status=r.status_code,
                    title=source["title"],
                    similarity=source["similarity"],
                    ext_urls=source["ext_urls"],
                    source=source["source"],
                    artist_name=source["artist"]["name"],
                    artist_url=source["artist"]["url"],
                )

                image.source_url = (
                    source["ext_urls"][0]
                    if source["ext_urls"] is not None and len(source["ext_urls"])
                    else None
                )

                source_hostname = urlparse(image.source_url).netloc

                source_names = {
                    "www.pixiv.net": "Pixiv",
                    "danbooru.donmai.us": "Danbooru",
                    "gelbooru.com": "Gelbooru",
                    "deviantart.com": "DevianArt",
                    "www.mangaupdates.com": "Manga Updates",
                    "mangadex.org": "Mangadex",
                    "yande.re": "yande.re",
                }

                image.source_name = (
                    source_names[source_hostname]
                    if source_hostname in source_names
                    else None
                )
                image.save()

                self.stdout.write(
                    f"QUERIED - Image ID: {image.id} - Results: {len(possible_sources)} - Status code: {r.status_code}"
                )
                self.stdout.write("Sleeping 10s...\n")
                time.sleep(10)
