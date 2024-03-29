from django.db.utils import IntegrityError
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

import requests

from nekosapi.images.models import Image


class Command(BaseCommand):
    help = "Import images from V2"

    def add_arguments(self, parser):
        parser.add_argument("api_token", type=str)

    def handle(self, api_token, *args, **options):
        i = getattr(Image.objects.order_by("-id").first(), "id", 0)

        while True:
            r = requests.get(
                f"https://v2.nekosapi.com/v2/images?sort=created_at&page[limit]=25&page[offset]={i}",
                headers={"Authorization": f"Bearer {api_token}"},
            )
            data = r.json()["data"]

            for image in data:
                im = Image.objects.create(
                    id_v2=image["id"],
                    image_v2=image["attributes"]["file"],
                    source=image["attributes"]["source"]["url"],
                    verification=Image.Verification.UNVERIFIED
                    if image["attributes"]["verificationStatus"] == "not_reviewed"
                    else image["attributes"]["verificationStatus"],
                    rating="suggestive"
                    if image["attributes"]["ageRating"] == "questionable"
                    else "safe"
                    if image["attributes"]["ageRating"] == "sfw"
                    else image["attributes"]["ageRating"],
                )

                self.stdout.write(f"Image {im.id} imported")
                del im

                i += 1
