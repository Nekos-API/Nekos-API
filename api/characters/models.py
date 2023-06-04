import uuid

from django.db import models
from django.db.models.functions import Lower
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Character(models.Model):
    """
    Character model.
    """

    class JSONAPIMeta:
        resource_name = "character"

    class Meta:
        indexes = [
            models.Index(Lower("first_name").desc(), Lower("last_name").desc(), name="character_name_index")
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False, editable=False)

    first_name = models.CharField(max_length=50, db_index=True)
    last_name = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    aliases = ArrayField(models.CharField(max_length=50), blank=True)

    description = models.CharField(max_length=512, null=True)

    gender = models.CharField(max_length=20, null=True, blank=True)
    species = models.CharField(max_length=20, default="Human", null=True)
    ages = ArrayField(models.SmallIntegerField(), blank=True)
    birth_date = models.CharField(
        max_length=14, null=True, blank=True
    )  # Max length: "September XXth"
    nationality = models.CharField(max_length=20, null=True, blank=True)
    occupations = ArrayField(models.CharField(max_length=100), blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.first_name}{' ' + self.last_name if self.last_name else ''}"
