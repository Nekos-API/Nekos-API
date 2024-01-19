from io import BytesIO

from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand

from deepdanbooru_onnx import DeepDanbooru

import requests
import PIL.Image

from nekosapi.images.models import Image, Tag
from nekosapi.characters.models import Character


danbooru = DeepDanbooru()


class Command(BaseCommand):
    help = "Use Deep Danbooru to tag images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--verbose",
            help="Logs output from DeepDanbooru",
            action="store_true",
        )

    def handle(self, verbose, *args, **options):
        qs = Image.objects.filter(danbooru_processed=False)
        count = qs.count()

        self.stdout.write("Enqueuing {} images to process.".format(count))

        i = 0

        for image in qs:
            try:
                img = PIL.Image.open(BytesIO(requests.get(image.image.url).content))
                danbooru_tags = danbooru(img)

                if verbose:
                    print("Deep Danbooru:", ', '.join([f"{k}: {v}" for k, v in danbooru_tags.items()]))

                t = [k for k, v in danbooru_tags.items() if v > 0.7]
                tags = Tag.objects.filter(danbooru_tags__overlap=t)
                characters = Character.objects.filter(danbooru_tags__overlap=t)

                if verbose:
                    print("Found tags:", [tag.name for tag in tags])
                    print("Found characters:", [character.name for character in characters])

                for tag in tags:
                    image.tags.add(tag)

                for character in characters:
                    image.characters.add(character)

                image.danbooru_processed = True
                image.save()

                i += 1

                self.stdout.write(
                    self.style.SUCCESS("SUCCESS")
                    + ": Processed image {} - {}".format(image.id, image.hash_md5)
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR("ERROR")
                    + ": Failed to process image {} - {}\n{}".format(
                        image.id, image.hash_md5, e
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("SUCCESS") + ": Processed {} images".format(i)
        )
