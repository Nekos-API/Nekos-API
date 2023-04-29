import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Artist(models.Model):
    """
    Artist model.
    """

    class JSONAPIMeta:
        resource_name = "artist"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)

    name = models.CharField(max_length=50, help_text="The artist's name")
    aliases = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        help_text="Other names the artist is known as.",
    )

    image = models.URLField(
        max_length=300, null=True, blank=True, help_text="The artist's avatar/profile picture."
    )

    links = ArrayField(
        models.URLField(max_length=256),
        help_text="Links to the artist's social media, website, pixiv, etc.",
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
