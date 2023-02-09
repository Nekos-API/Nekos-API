from django.db import models
from oauth2_provider.models import AbstractApplication

from dynamic_filenames import FilePattern

from django_resized import ResizedImageField

# Create your models here.


class Application(AbstractApplication):
    """
    Extends the default Django OAuth Toolkit application model.
    """

    icon = ResizedImageField(
        size=[1024, 1024],
        crop=["middle", "center"],
        upload_to=FilePattern(
            filename_pattern="uploads/applications/icons/{uuid:base32}{ext}"
        ),
        blank=True,
        null=True,
    )

    description = models.CharField(max_length=500, blank=True, null=True)
