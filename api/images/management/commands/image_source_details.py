from urllib.parse import urlparse, parse_qs

import os, uuid, io

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

import dotenv

import requests

import PIL

import imagehash

from images.models import Image


dotenv.load_dotenv()


source_names = {
    "pixiv.net": "Pixiv",
    "danbooru.donmai.us": "Danbooru",
    "gelbooru.com": "Gelbooru",
    "deviantart.com": "DevianArt",
    "mangaupdates.com": "Manga Updates",
    "mangadex.org": "Mangadex",
    "yande.re": "yande.re",
    "patreon.com": "Patreon",
    "reddit.com": "Reddit",
    "instagram.com": "Instagram",
}


class Command(BaseCommand):
    help = "Fetches all the details possible from different APIs"

    def add_arguments(self, parser):
        parser.add_argument("image_id", help="The image's ID", type=uuid.UUID)

    def handle(self, *args, **options):
        """
        Fetches all the possible image details.
        """

        image = Image.objects.get(id=options["image_id"])

        self.stdout.write(f"Fetching details for image {image.id}: {image.title}")

        match urlparse(image.source_url).netloc:
            case "gelbooru.com":
                return self.handle_data_update(image, GelbooruAPI(image))
            case "danbooru.donmai.us":
                return self.handle_data_update(image, DanbooruAPI(image))
            case _:
                self.stdout.write("Unknown source.")

    def handle_data_update(self, image: Image, api):
        self.stdout.write(f"Fetching details from {api.name}...")

        details = api.get_post_details(image.source_url)

        if details:
            if api.is_current_file_small(details):
                self.stdout.write("File is smaller than the current file. Replacing...")
                api.replace_current_file(details)
                self.stdout.write("Replaced current file!")

            new_source = api.get_source(details)
            if new_source:
                parsed_source = urlparse(new_source)

                image.source_url = new_source
                image.source_name = (
                    source_names.get(parsed_source.netloc)
                    if parsed_source.netloc
                    else source_names.get("www." + parsed_source.netloc, None)
                )
                image.save()
                self.stdout.write("Updated source!")
        else:
            self.stdout.write("No details found.")


class GelbooruAPI:
    base_url = "https://gelbooru.com/index.php?page=dapi&q=index&json=1"
    name = "Gelbooru"

    def __init__(self, image):
        self.image = image

    def get_post_details(self, url: str) -> dict:
        """
        Fetches the post's details from gelbooru's API.
        """

        post_id = int(parse_qs(urlparse(url).query)["id"][0])

        r = requests.get(
            f"{self.base_url}&s=post&id={post_id}",
        )

        if r.status_code == 200:
            return r.json()["post"][0]
        else:
            return None

    def is_current_file_small(self, details) -> bool:
        """
        Checks if gelbooru's file is bigger (higher res) than the current file.
        """

        return (
            self.image.height <= details["height"]
            and self.image.width <= details["width"]
        )

    def replace_current_file(self, details) -> bool:
        """
        Downloads the new file from gelbooru and replaces the current file with it.
        """

        url = details["file_url"]

        r = requests.get(url)

        if r.status_code == 200:
            self.image.file = File(r.content, self.image.title)
            self.image.height = details["height"]
            self.image.width = details["width"]
            self.hash_perceptual = str(
                imagehash.phash(PIL.Image.open(io.BytesIO(r.content)), hash_size=16)
            )
            self.image.save()
            return True
        else:
            return False

    def get_source(self, details) -> str:
        """
        Returns the source of the image.
        """
        return details["source"]


class DanbooruAPI:
    name = "Danbooru"

    def __init__(self, image):
        self.image = image

    def get_post_details(self, url: str) -> dict:
        """
        Fetches the post's details from danbooru's API.
        """

        r = requests.get(
            f"https://danbooru.donmai.us/posts/{url.rsplit('/', 1)[1]}.json",
        )

        if r.status_code == 200:
            return r.json()
        else:
            return None

    def is_current_file_small(self, details) -> bool:
        """
        Checks if danbooru's file is bigger (higher res) than the current file.
        """

        return (
            self.image.height <= details["image_height"]
            and self.image.width <= details["image_width"]
        )

    def replace_current_file(self, details) -> bool:
        """
        Downloads the new file from danbooru and replaces the current file with it.
        """

        url = details["large_file_url"]

        r = requests.get(url)

        if r.status_code == 200:
            self.image.file = File(io.BytesIO(r.content), self.image.title)
            self.image.height = details["image_height"]
            self.image.width = details["image_width"]
            self.hash_perceptual = str(
                imagehash.phash(PIL.Image.open(io.BytesIO(r.content)), hash_size=16)
            )
            self.image.save()
            return True
        else:
            return False

    def get_source(self, details) -> str:
        """
        Returns the source of the image.
        """
        return details["source"]
