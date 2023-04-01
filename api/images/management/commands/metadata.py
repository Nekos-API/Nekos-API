from django.core.management.base import BaseCommand, CommandError
from django.db.models import F, Q

import requests

from images.models import Image

class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Loads metadata to images
        """

        images = Image.objects.filter(Q(mimetype__isnull=True) | Q(file_size__isnull=True)).exclude(Q(file__isnull=True) | Q(file=""))
        
        total_images = images.count()
        j = 1

        for image in images:
            self.stdout.write(
                self.style.WARNING("LOADING: DOWNLOADING")
                + f" - {image.id} - ({j}/{total_images})",
                ending="\r",
            )

            r = requests.head(image.file.url)

            content_type = r.headers.get("Content-Type")
            file_size = r.headers.get("Content-Length")
            
            image.mimetype = content_type
            image.file_size = file_size
            image.save()
            
            self.stdout.write(
                self.style.SUCCESS("SUCCESS")
                + f" - {image.id} - {content_type} - {file_size} bytes - ({j}/{total_images})"
            )
            j += 1
