import uuid
import secrets

from urllib.parse import urlparse

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

        ON_CATEGORY_CREATE = "on-category-create"
        ON_CATEGORY_UPDATE = "on-category-update"
        ON_CATEGORY_DELETE = "on-category-delete"

        ON_CHARACTER_CREATE = "on-character-create"
        ON_CHARACTER_UPDATE = "on-character-update"
        ON_CHARACTER_DELETE = "on-character-delete"

    def validate_url(value):
        if urlparse(value).scheme != "https":
            raise ValidationError("The webhook URL's scheme can only be https.")

    def generate_token():
        """
        Returns a 256-character-long URL-safe token.
        """
        return secrets.token_urlsafe(192)

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    name = models.CharField(max_length=256)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    events = ArrayField(
        models.CharField(max_length=19, choices=Event.choices),
        blank=False,
    )

    url = models.CharField(max_length=256, validators=[validate_url])

    verification_key = models.CharField(max_length=256, default=generate_token)
