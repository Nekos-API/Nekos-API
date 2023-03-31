import io

from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q

from colorthief import ColorThief

import requests

from images.models import Image


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Sets the color palette of an image.
        """
        images = Image.objects.filter(Q(dominant_color__isnull=True) | Q(palette__isnull=True), verification_status="verified").exclude(Q(file="") | Q(file__isnull=True))
        total_images = images.count()

        j = 1

        for image in images:
            ct = ColorThief(io.BytesIO(requests.get(image.file.url).content))
            dominant = ct.get_color(quality=1)
            palette = ct.get_palette(color_count=10, quality=1)

            image.dominant_color = list(dominant)
            image.palette = list(palette)
            image.save()

            self.stdout.write(self.style.SUCCESS("SUCCESS") + f" - {image.id} - {image.dominant_color} - ({j}/{total_images})")
            j += 1
