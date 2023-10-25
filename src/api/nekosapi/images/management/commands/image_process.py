from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand

from nekosapi.images.models import Image


class Command(BaseCommand):
    help = "Process all unprocessed images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            help="Delete duplicates (using md5 hash)",
            action="store_true",
        )

    def handle(self, delete = False, *args, **options):
        qs = Image.objects.filter(image_height__isnull=True, image_width__isnull=True)
        count = qs.count()

        self.stdout.write("Enqueuing {} images to process.".format(count))

        i = 0

        for image in qs:
            try:
                image.process()
                i += 1

                self.stdout.write(
                    self.style.SUCCESS("SUCCESS")
                    + ": Processed image {} - {}".format(image.id, image.hash_md5)
                )
            except IntegrityError:
                if delete:
                    self.stdout.write(
                        self.style.ERROR("DELETED")
                        + ": Failed to process image {} - {}".format(
                            image.id, image.hash_md5
                        )
                    )
                    image.delete()
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
