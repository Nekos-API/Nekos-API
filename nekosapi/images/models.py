from django.db import models
from django.contrib.postgres.fields import ArrayField

from dynamic_filenames import FilePattern


class Image(models.Model):
    class Rating(models.TextChoices):
        SAFE = "safe", "Safe"
        SUGGESTIVE = "suggestive", "Suggestive"
        BORDERLINE = "borderline", "Borderline"
        EXPLICIT = "explicit", "Explicit"

    file = models.ImageField(
        upload_to=FilePattern(filename_pattern="images/original/{uuid}{ext}")
    )
    rating = models.CharField(
        max_length=10, choices=Rating.choices, default=Rating.SAFE
    )

    color_dominant = ArrayField(models.SmallIntegerField(), size=3, default=list)
    color_palette = ArrayField(
        ArrayField(models.SmallIntegerField(), size=3), size=10, default=list
    )

    artist_name = models.CharField(max_length=100, blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=100), default=list)

    source_name = models.CharField(max_length=100, blank=True, null=True)
    source_id = models.CharField(max_length=100, blank=True, null=True)
