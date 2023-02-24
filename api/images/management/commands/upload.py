import os

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from images.models import Image
from users.models import User
from artists.models import Artist

class Command(BaseCommand):

    help = "Uploads all images from the `upload/` folder in the project's root"

    def add_arguments(self, parser):
        parser.add_argument('uploader', help="The uploader's username")
        parser.add_argument('artist', help="The artist's name", default="")

    def handle(self, *args, **options):
        """
        Uploads the images.
        """

        total = len(list(os.scandir('./upload/')))

        i = 0

        uploader = User.objects.get(username=options['uploader'])
        artist = Artist.objects.filter(name=options['artist']).first()

        self.stdout.write(f"Uploading {total} images{'' if not artist else f' by {artist.name}'} in the name of user {uploader.username}...\n")

        for image in os.scandir('./upload/'):
            i += 1

            if Image.objects.filter(title=f"Uploaded by {uploader.username} - {image.name}"[:100]).exists():
                self.stdout.write(f"Skipped - ({i}/{total})")
                continue
                
            obj = Image.objects.create(
                title=f"Uploaded by {uploader.username} - {image.name}"[:100],
                uploader=uploader,
                artist=artist,
                verification_status=Image.VerificationStatus.NOT_REVIEWED,
                file=File(open(image.path, 'rb'), image.name)
            )

            self.stdout.write(f"UPLOADED - {obj.id} - ({i}/{total})")
        
        self.stdout.write(f"\nSuccessfully uploaded {total} images.")