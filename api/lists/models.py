import uuid

from django.db import models

# Create your models here.


class List(models.Model):
    """
    List of images.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)

    user = models.ForeignKey(
        "users.User", related_name="image_lists", on_delete=models.CASCADE
    )
    is_private = models.BooleanField(default=False)

    images = models.ManyToManyField("images.Image", related_name="image_lists", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
