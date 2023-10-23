from django.core.management.base import BaseCommand
from django.core.files import File

import requests

from nekosapi.images.models import Image


class Command(BaseCommand):
    help = "Import images from V2"

    def add_arguments(self, parser):
        parser.add_argument("api_token", type=str)

    def handle(self, api_token, *args, **options):
        i = 0

        while True:
            r = requests.get(
                f"https://v2.nekosapi.com/v2/images?page[offset]={i * 25}",
                headers={"Authorization": f"Bearer {api_token}"},
            )
            data = r.json()["data"]

            for image in data:
                image = Image.objects.create(
                    image=File(requests.get(image["attributes"]["file"]).content),
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
                self.stdout.write(f"Image {image.id} imported")
                del image

            i += 1
