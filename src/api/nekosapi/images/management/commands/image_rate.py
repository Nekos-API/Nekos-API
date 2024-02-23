import io

from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand

import PIL.Image

import requests

from nekosapi.images.models import Image


class Command(BaseCommand):
    help = "Rates all the images using NSFW.JS API"

    def add_arguments(self, parser):
        parser.add_argument(
            "url",
            help="URL of the NSFW.JS API",
        )
        parser.add_argument(
            "--all",
            help="Process all images even if already verified",
            action="store_true",
        )

    def handle(self, url, all, *args, **options):
        uv = (
            Image.objects.filter(verification=Image.Verification.UNVERIFIED)
            if not all
            else Image.objects.all()
        )
        total = uv.count()
        print(f"Processing {total} images...")

        i = 1

        for image in uv:
            imgb = requests.get(image.image.url).content

            try:
                imgp = PIL.Image.open(io.BytesIO(imgb))
                imgp.convert("RGBA")
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR("ERROR")
                    + ": Failed to open image {}\n{}".format(image.id, e)
                )
                continue

            buffer = io.BytesIO()
            imgp.save(buffer, format="PNG")
            buffer.seek(0)

            try:
                classification = requests.post(
                    url, files={"image": ("image.png", buffer)}
                ).json()
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR("ERROR")
                    + ": Failed to fetch classification {}\n{}".format(image.id, e)
                )
                continue

            hentai_rating = classification["hentai"]
            sexy_rating = classification["sexy"]

            if hentai_rating > 0.85:
                image.rating = Image.Rating.EXPLICIT
                image.verification = Image.Verification.VERIFIED
                image.save()
            elif hentai_rating > 0.60:
                image.rating = Image.Rating.BORDERLINE
                image.verification = Image.Verification.VERIFIED
                image.save()
            elif hentai_rating > 0.30 or sexy_rating > 0.5:
                image.rating = Image.Rating.SUGGESTIVE
                image.verification = Image.Verification.VERIFIED
                image.save()
            else:
                image.rating = Image.Rating.SAFE
                image.verification = Image.Verification.VERIFIED
                image.save()

            self.stdout.write(
                self.style.SUCCESS("SUCCESS")
                + ": ({}/{}) Processed image {} - {}".format(i, total, image.id, image.rating)
            )
            i += 1
