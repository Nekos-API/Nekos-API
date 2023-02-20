import os

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from images.models import Image
from users.models import User

class Command(BaseCommand):

    help = "Uploads all images from the `upload/` folder in the project's root"

    def add_arguments(self, parser):
        parser.add_argument('uploader', help="The uploader's username")

    def handle(self, *args, **options):
        """
        Uploads the images.
        """

        total = len(list(os.scandir('./upload/')))

        i = 0

        print(f"Uploading {total} images in the name of user {options['uploader']}...")

        uploader = User.objects.get(username=options['uploader'])

        for image in os.scandir('./upload/'):
            i += 1

            if Image.objects.filter(title=f"Uploaded by {uploader.username} - {image.name}"[:100]).exists():
                print(f"Skipped - ({i}/{total})")
                continue
                
            obj = Image.objects.create(
                title=f"Uploaded by {uploader.username} - {image.name}"[:100],
                uploader=uploader,
                verification_status=Image.VerificationStatus.NOT_REVIEWED,
                file=File(open(image.path, 'rb'), image.name)
            )

            self.stdout.write(f"UPLOADED - {obj.id} - ({i}/{total})")