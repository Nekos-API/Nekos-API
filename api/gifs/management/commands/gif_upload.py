"""
Uploaded up to: 1019
"""

import os
import json

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from gifs.models import Gif, Reaction
from users.models import User


class Command(BaseCommand):
    help = "Uploads all gifs from the `uploads/` folder in the project's root"

    def add_arguments(self, parser):
        parser.add_argument("uploader", help="The uploader's username")
        parser.add_argument("--start", help="The number of GIFs to skip", type=int)

    def handle(self, *args, **options):
        """
        Uploads the images.
        """

        total = len(list(os.scandir("./uploads/")))

        i = 0

        uploader = User.objects.get(username=options["uploader"])

        self.stdout.write(
            f"Uploading {total} gifs in the name of user {uploader.username}...\n"
        )

        for gif in os.scandir("./uploads/"):
            if gif.name.endswith('.json'):
                continue

            if options["start"] is not None and i < options["start"]:
                i += 1
                continue

            reactions = []

            try:
                gif_num = int(gif.name.split('.')[0])
                gif_data = json.load(open(f"{gif_num}.json", "r"))

                for tag in gif_data.get("edited_tags", []):
                    tag_obj = Reaction.objects.filter(name__iexact=tag).first()
                    if tag_obj:
                        reactions.append(tag_obj)

                for tag in gif_data.get("tags", []):
                    tag_obj = Reaction.objects.filter(name__iexact=tag).first()
                    if tag_obj:
                        reactions.append(tag_obj)
            except:
                pass

            obj = Gif.objects.create(
                uploader=uploader,
                verification_status=Gif.VerificationStatus.NOT_REVIEWED,
                file=File(open(gif.path, "rb"), gif.name),
            )
            obj.reactions.set(reactions)
            obj.save()

            self.stdout.write(f"UPLOADED - {obj.id} - ({i}/{total})")

            i += 1

        self.stdout.write(f"\nSuccessfully uploaded {total} gifs.")
