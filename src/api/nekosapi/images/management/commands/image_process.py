from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Process all unprocessed images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            help="Delete duplicates (using md5 hash)",
            action="store_true",
            type=bool,
        )

    def handle(self, *args, **options):
        qs = Image.objects.filter(image_height__isnull=True, image_width__isnull=True)
        count = qs.count()

        self.stdout.write("Enqueuing {} images to process.".format(count))

        i = 0

        for image in qs:
            try:
                image.process()
                i += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR("ERROR")
                    + ": Failed to process image {} - {}\n{}".format(
                        image.id, image.hash_md5, e
                    )
                )

            self.stdout.write(
                self.style.SUCCESS("SUCCESS")
                + ": Processed image {} - {}".format(image.id, image.hash_md5)
            )

        self.stdout.write(
            self.style.SUCCESS("SUCCESS") + ": Processed {} images".format(i)
        )
