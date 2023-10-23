from django.db import models
from django.contrib.postgres.fields import ArrayField

from dynamic_filenames import FilePattern


class Artist(models.Model):
    name = models.TextField()
    image = models.ImageField(
        upload_to=FilePattern(filename_pattern="artists/original/{filename}{ext}"),
        null=True,
        blank=True,
    )
    aliases = ArrayField(models.TextField(), blank=True)
    links = ArrayField(models.URLField(), blank=False)
    policy_repost = models.BooleanField(null=True)
    policy_credit = models.BooleanField(default=True)
    policy_ai = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
