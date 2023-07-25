import io

from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q

import PIL

import requests

import imagehash

from images.models import Image


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Sets the color palette of an image.
        """
        images = Image.objects.filter(hash_perceptual__isnull=True).exclude(
            Q(file="") or Q(file__isnull=True)
        )
        total_images = images.count()

        j = 1

        for image in images:
            self.stdout.write(
                self.style.WARNING("LOADING: DOWNLOADING")
                + f" - {image.id} - {image.height}x{image.width} - ({j}/{total_images})",
                ending="\r",
            )

            f = io.BytesIO(requests.get(image.file.url).content)
            img = PIL.Image.open(f)

            self.stdout.write(
                self.style.WARNING("LOADING: PERCEPTUAL")
                + f" - {image.id} - {image.height}x{image.width} - ({j}/{total_images})"
                + " " * 10,
                ending="\r",
            )

            perceptual_hash = imagehash.phash(img, hash_size=16)
            image.hash_perceptual = perceptual_hash

            image.save()
            f.close()

            self.stdout.write(
                self.style.SUCCESS("SUCCESS")
                + f" - {image.id} - {image.hash_perceptual} - ({j}/{total_images})"
                + " " * 10
            )
            j += 1
