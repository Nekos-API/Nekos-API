import io
import os
import tempfile

from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q

from nudenet import NudeClassifier

from rich import print

import requests

from images.models import Image


class Command(BaseCommand):
    def handle(self, *args, **options):
        classifier = NudeClassifier()

        try:
            os.mkdir("./ai_tmp_imgs")
        except FileExistsError:
            pass

        for image in (
            Image.objects.filter(age_rating=None).exclude(file="").exclude(file=None)
        ):
            file_name = f"./ai_tmp_imgs/{image.file.url.rsplit('/', 1)[1]}"

            r = requests.get(image.file.url)
            f = open(file_name, "w+b")

            f.write(r.content)

            f.close()

            try:
                classification = classifier.classify(file_name)

                unsafe = classification[file_name]["unsafe"]

                if unsafe < 0.15:
                    image.age_rating = Image.AgeRating.SFW
                elif unsafe < 0.45:
                    image.age_rating = Image.AgeRating.QUESTIONABLE
                elif unsafe < 0.7:
                    image.age_rating = Image.AgeRating.SUGGESTIVE
                elif unsafe < 0.9:
                    image.age_rating = Image.AgeRating.BORDERLINE
                else:
                    image.age_rating = Image.AgeRating.EXPLICIT

                image.save()
                print(image.id, "-", image.file.url, "-", image.age_rating, "-", unsafe)
            except Exception as e:
                self.stderr.write("ERROR - Could not process image")

            os.remove(file_name)

        os.rmdir("./ai_tmp_imgs")
