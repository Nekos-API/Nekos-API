import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

from dynamic_filenames import FilePattern

# Create your models here.


class Gif(models.Model):
    """
    Gif model.
    """

    class JSONAPIMeta:
        resource_name = "gif"

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

    class Emotion(models.TextChoices):
        SADNESS = "sadness"
        HAPPINESS = "happiness"
        FEAR = "fear"
        ANGER = "anger"
        SURPRISE = "surprise"
        DISGUST = "disgust"

    def validate_rgb_value(value):
        if value not in range(0, 256):
            raise ValidationError(
                detail="This is not a valid RGB value (0-255)",
                code="invalid_rgb_value",
                params={"value": value},
            )

    id = models.UUIDField(
        default=uuid.uuid4, null=False, editable=False, primary_key=True
    )

    file = models.FileField(
        upload_to=FilePattern(filename_pattern="gifs/{uuid:base32}{ext}")
    )

    age_rating = models.CharField(
        max_length=12,
        choices=AgeRating.choices,
        null=True,
        blank=True,
        help_text="The image's sfw-ness.",
        db_index=True,
    )

    verification_status = models.CharField(
        default=VerificationStatus.NOT_REVIEWED,
        choices=VerificationStatus.choices,
        max_length=12,
        null=False,
        blank=False,
        help_text="The image's verification status.",
        db_index=True,
    )

    duration = models.FloatField(null=True, blank=True)

    emotions = ArrayField(
        models.CharField(max_length=30, null=False, choices=Emotion.choices),
        blank=True,
        default=list,
        help_text=f"{', '.join(e[1] for e in Emotion.choices)}",
        db_index=True,
    )

    source_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="The name of the platform where the original post was posted.",
    )
    source_url = models.URLField(
        null=True, help_text="The image's original post.", blank=True
    )

    dominant_color = ArrayField(
        models.SmallIntegerField(),
        size=3,
        null=True,
        blank=True,
        validators=[validate_rgb_value],
    )
    palette = ArrayField(
        ArrayField(
            models.SmallIntegerField(),
            size=3,
            null=False,
            blank=False,
            validators=[validate_rgb_value],
        ),
        size=10,
        null=True,
        blank=True,
    )

    height = models.SmallIntegerField(
        default=0, help_text="The gif's height in pixels."
    )
    width = models.SmallIntegerField(default=0, help_text="The gif's width in pixels.")
    aspect_ratio = models.CharField(
        max_length=20,
        help_text="The gif's aspect ratio (w:h).",
        null=True,
        blank=True,
    )
    orientation = models.CharField(
        max_length=9, blank=True, null=True, choices=Orientation.choices
    )

    mimetype = models.CharField(
        max_length=11, null=True, blank=True, help_text="The image's file format."
    )
    file_size = models.PositiveIntegerField(
        null=True, blank=True, help_text="The file size in bytes of the image file."
    )
    frames = models.PositiveIntegerField(
        null=True, blank=True, help_text="The amount of frames that the GIF has."
    )

    text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="A reaction message that you'd see with the gif. For example: '$1 is patting $2!'. $1 and $2 are persons and will be replaced by the API user.",
    )

    is_spoiler = models.BooleanField(default=False)

    reactions = models.ManyToManyField("gifs.Reaction", related_name="gifs", blank=True)

    categories = models.ManyToManyField(
        "categories.Category", related_name="gifs", blank=True
    )
    characters = models.ManyToManyField(
        "characters.Character", related_name="gifs", blank=True
    )

    uploader = models.ForeignKey("users.User", models.CASCADE, related_name="gifs")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reaction(models.Model):
    """
    Reaction model.
    """

    class JSONAPIMeta:
        resource_name = "reaction"

    id = models.UUIDField(
        default=uuid.uuid4, null=False, editable=False, primary_key=True
    )

    name = models.CharField(
        max_length=100,
        help_text="Keep it neutral (?). For example, <b>Wave</b> but not <b>Waving</b>.",
        unique=True,
        db_index=True,
    )

    is_nsfw = models.BooleanField(
        default=False, help_text="Wether the reaction is NSFW or not."
    )

    def __str__(self) -> str:
        return self.name
