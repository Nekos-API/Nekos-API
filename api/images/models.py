import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField

from django_resized import ResizedImageField

from dynamic_filenames import FilePattern

# Create your models here.


class Image(models.Model):
    """
    Image model.
    """

    class JSONAPIMeta:
        resource_name = "image"

    class AgeRating(models.TextChoices):
        """
        Age rating text choices.
        """

        SFW = "sfw"
        QUESTIONABLE = "questionable"
        SUGGESTIVE = "suggestive"
        BORDERLINE = "borderline"
        EXPLICIT = "explicit"

    class VerificationStatus(models.TextChoices):
        """
        Verification status choices.
        """

        NOT_REVIEWED = "not_reviewed"
        ON_REVIEW = "on_review"
        DECLINED = "declined"
        VERIFIED = "verified"

    class Orientation(models.TextChoices):
        LANDSCAPE = "landscape"
        PORTRAIT = "portrait"
        SQUARE = "square"

    def validate_rgb_value(value):
        if value not in range(0, 256):
            raise ValidationError(
                detail="This is not a valid RGB value (0-255)",
                code="invalid_rgb_value",
                params={"value": value},
            )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    file = ResizedImageField(
        upload_to=FilePattern(filename_pattern="uploads/images/{uuid:base32}{ext}")
    )

    title = models.CharField(max_length=100)

    # If an artist requests it's data deletion, all their images will be
    # automatically deleted together with the Artist record.
    artist = models.ForeignKey(
        "artists.Artist",
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
    )

    height = models.SmallIntegerField(
        default=0, help_text="The image's height in pixels."
    )
    width = models.SmallIntegerField(
        default=0, help_text="The image's width in pixels."
    )
    aspect_ratio = models.CharField(
        max_length=20,
        help_text="The image's aspect ratio (w:h).",
        null=True,
        blank=True,
    )
    orientation = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        choices=Orientation.choices
    )

    source_url = models.URLField(
        null=True, help_text="The image's original post.", blank=True
    )
    source_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="The name of the platform where the original post was posted.",
    )

    age_rating = models.CharField(
        max_length=12,
        choices=AgeRating.choices,
        null=True,
        blank=True,
        help_text="The image's sfw-ness.",
    )

    is_original = models.BooleanField(
        default=False,
        help_text="Wether the image was illustrated by the original artist of the characters that appear in it.",
    )

    verification_status = models.CharField(
        default=VerificationStatus.NOT_REVIEWED,
        choices=VerificationStatus.choices,
        max_length=12,
        null=False,
        blank=False,
        help_text="The image's verification status.",
    )

    dominant_color = ArrayField(
        models.SmallIntegerField(),
        size=3,
        null=True,
        blank=True,
        validators=[validate_rgb_value],
    )
    primary_color = ArrayField(
        models.SmallIntegerField(),
        size=3,
        null=True,
        blank=True,
        validators=[validate_rgb_value],
    )

    characters = models.ManyToManyField(
        "characters.Character", related_name="images", blank=True
    )
    categories = models.ManyToManyField(
        "categories.Category", related_name="images", blank=True
    )

    uploader = models.ForeignKey(
        "users.User",
        related_name="uploaded_images",
        null=False,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class ImageSourceResult(models.Model):
    """
    Stores a query from SauceNAO.
    """

    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )

    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="source_queries"
    )

    status = models.SmallIntegerField(default=400)
    
    title = models.CharField(max_length=256, null=True, blank=True)
    similarity = models.FloatField()
    ext_urls = ArrayField(models.URLField(max_length=500), blank=True, null=True)
    source = models.CharField(max_length=256, null=True, blank=True)
    artist_name = models.CharField(max_length=256, null=True, blank=True)
    artist_url = models.CharField(max_length=256, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Query from SauceNAO for {self.image.id} (Status code: {self.status})"
        )
