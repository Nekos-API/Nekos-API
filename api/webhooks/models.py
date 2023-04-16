import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Webhook(models.Model):
    class Event(models.TextChoices):
        ON_IMAGE_CREATE = "on-image-create"
        ON_IMAGE_UPDATE = "on-image-update"
        ON_IMAGE_DELETE = "on-image-delete"

        ON_ARTIST_CREATE = "on-artist-create"
        ON_ARTIST_UPDATE = "on-artist-update"
        ON_ARTIST_DELETE = "on-artist-delete"

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    name = models.CharField(max_length=256)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    events = ArrayField(
        models.CharField(max_length=16, choices=Event.choices),
        blank=False,
    )

    urls = ArrayField(models.CharField(max_length=256), blank=False)
