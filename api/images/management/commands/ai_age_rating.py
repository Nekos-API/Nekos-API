import io
import os
import tempfile

from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q

from nudenet import NudeDetector

from rich import print

import requests

from images.models import Image


class Command(BaseCommand):
    def handle(self, *args, **options):
        detector = NudeDetector()

        try:
            os.mkdir("./ai_tmp_imgs")
        except FileExistsError:
            pass

        for image in Image.objects.filter(age_rating=None):
            print(image.file.url)

            file_name = f"./ai_tmp_imgs/{image.file.url.rsplit('/', 1)[1]}"

            r = requests.get(image.file.url)
            f = open(file_name, "w+b")

            f.write(r.content)

            f.close()

            try:
                print(detector.detect(file_name))
            except:
                self.stderr.write("ERROR - Could not process image")

            os.remove(file_name)
