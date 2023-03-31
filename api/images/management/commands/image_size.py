import io
import os
import time
import PIL.Image

from django.core.management.base import BaseCommand, CommandError

import requests

from images.models import Image


def get_aspect_ratio(height: int, width: int):
    """
    Returns the aspect ratio of an image.
    """
    divider = 0
    i = height if height > width else width

    while i != 0:
        if height % i == 0 and width % i == 0:
            divider = i
            break
        i -= 1

    return f"{int(width / divider)}:{int(height / divider)}"


class Command(BaseCommand):
    def handle(self, *args, **options):
        images = Image.objects.filter(height=0, width=0).exclude(file=None)
        total_images = images.count()

        j = 1

        for image in images:
            r = requests.get(image.file.url)
            f = io.BytesIO(r.content)
            pil_image = PIL.Image.open(f)

            image.height = pil_image.height
            image.width = pil_image.width

            pil_image.close()

            image.aspect_ratio = get_aspect_ratio(image.height, image.width)

            image.save()

            self.stdout.write(
                self.style.SUCCESS("SUCCESS")
                + f" - {image.id} - {image.height}x{image.width} [{image.aspect_ratio}] - ({j}/{total_images})"
            )
            j += 1
