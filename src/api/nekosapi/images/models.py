from io import BytesIO

import hashlib

from django.db import models
from django.core.files.images import ImageFile
from django.contrib.postgres.fields import ArrayField

from dynamic_filenames import FilePattern

from colorthief import ColorThief

import imagehash

import PIL.Image

import requests


def _make_sample(im: PIL.Image, size: tuple) -> ImageFile:
    """Generate a sample/thumbnail image.

    Args:
        image (_type_): The image to generate the sample from.
        size (tuple): The size of the sample.

    Returns:
        File: The sample.
    """
    if None not in size:
        im.thumbnail(size)
    elif size[0] is None:
        # Mantain the aspect ratio
        im.thumbnail((((size[1] * im.width) // im.height), size[1]))
    else:
        # Mantain the aspect ratio
        im.thumbnail((size[0], ((size[0] * im.height) // im.width)))

    sample_io = BytesIO()

    im.save(sample_io, "WEBP", quality=100)

    sample_io.seek(0)

    return ImageFile(sample_io, name="sample.webp")


def _to_webp(im: PIL.Image) -> ImageFile:
    """Convert an image to webp.

    Args:
        image (_type_): The image to convert.

    Returns:
        File: The converted image.
    """

    webp_io = BytesIO()

    im.save(webp_io, "WEBP", quality=100)

    webp_io.seek(0)

    return ImageFile(webp_io, name="img.webp")


class Image(models.Model):
    class Verification(models.TextChoices):
        VERIFIED = "verified", "Verified"
        ON_REVIEW = "on_review", "On review"
        DECLINED = "declined", "Declined"
        UNVERIFIED = "unverified", "Unverified"

    class Rating(models.TextChoices):
        SAFE = "safe", "Safe"
        SUGGESTIVE = "suggestive", "Suggestive"
        BORDERLINE = "borderline", "Borderline"
        EXPLICIT = "explicit", "Explicit"

    id_v2 = models.UUIDField("ID v2", null=True)
    image_v2 = models.URLField("Image URL v2", null=True)

    image = models.ImageField(
        upload_to=FilePattern(filename_pattern="images/original/{uuid}{ext}"),
        null=True,
        blank=True,
    )
    sample = models.ImageField(
        upload_to=FilePattern(filename_pattern="images/360/{uuid}{ext}"),
        null=True,
        blank=True,
    )

    image_size = models.PositiveIntegerField(null=True)
    image_width = models.PositiveIntegerField(null=True)
    image_height = models.PositiveIntegerField(null=True)
    sample_size = models.PositiveIntegerField(null=True)
    sample_width = models.PositiveIntegerField(null=True)
    sample_height = models.PositiveIntegerField(null=True)

    source = models.TextField(null=True)
    source_id = models.PositiveIntegerField(null=True)

    verification = models.CharField(
        choices=Verification.choices,
        max_length=10,
        default=Verification.UNVERIFIED,
    )

    rating = models.CharField(choices=Rating.choices, max_length=12, null=True)

    hash_md5 = models.CharField(max_length=32, null=True, unique=True)
    hash_perceptual = models.CharField(max_length=32, null=True)

    color_dominant = ArrayField(
        models.PositiveSmallIntegerField(),
        size=3,
        null=True,
    )
    color_palette = ArrayField(
        ArrayField(
            models.PositiveSmallIntegerField(),
            size=3,
        ),
        size=10,
        null=True,
    )

    duration = models.PositiveIntegerField(null=True, blank=True)

    is_original = models.BooleanField(default=False)
    is_screenshot = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    is_animated = models.BooleanField(default=False)

    artist = models.ForeignKey(
        "artists.Artist", on_delete=models.CASCADE, related_name="images", null=True
    )

    characters = models.ManyToManyField(
        "characters.Character", blank=True, related_name="images"
    )

    tags = models.ManyToManyField("Tag", blank=True, related_name="images")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def process(self):
        file = BytesIO(requests.get(self.image_v2).content)
        image = PIL.Image.open(file)

        self.image = _to_webp(image)
        self.sample = _make_sample(image, (360, None))

        self.image_size = self.image.size
        self.sample_size = self.sample.size
        self.image_width = image.size[0]
        self.image_height = image.size[1]
        self.sample_width = self.sample.width
        self.sample_height = self.sample.height

        file.seek(0)
        thief = ColorThief(file)
        self.color_dominant = list(thief.get_color(quality=1))
        self.color_palette = [
            list(color) for color in thief.get_palette(color_count=10, quality=1)
        ]

        file.seek(0)
        self.hash_md5 = hashlib.md5(file.read()).hexdigest()
        self.hash_perceptual = str(imagehash.phash(image))

        self.is_animated = image.is_animated
        self.duration = image.n_frames if image.is_animated else None

        self.save()


class Tag(models.Model):
    id_v2 = models.UUIDField(null=True)

    name = models.CharField(max_length=255)
    description = models.TextField()
    is_nsfw = models.BooleanField(default=False)

    def __str__(self):
        return self.name
