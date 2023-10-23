from django.db import models
from django.contrib.postgres.fields import ArrayField


class Character(models.Model):
    name = models.TextField(
        help_text="The character's complete name. Last name first, followed by a comma, followed by the first name."
    )
    aliases = ArrayField(
        models.TextField(),
        blank=True,
        help_text="Other names the character is officially known as.",
    )
    description = models.TextField(
        null=True, help_text="A brief description of the character."
    )
    ages = ArrayField(
        models.PositiveSmallIntegerField(),
        blank=True,
        help_text="All the ages the character offically has/has officially had.",
    )
    height = models.PositiveSmallIntegerField(
        null=True, help_text="The character's height in cm."
    )
    weight = models.PositiveSmallIntegerField(
        null=True, help_text="The character's weight in kg."
    )
    gender = models.TextField(null=True, help_text="The character's gender.")
    species = models.TextField(
        default="Human", null=True, help_text="The character's species."
    )
    birthday = models.DateField(
        null=True, help_text="The character's birthday. Year doesn't matter."
    )
    nationality = models.TextField(null=True, help_text="The character's nationality.")
    occupations = ArrayField(
        models.TextField(),
        blank=True,
        help_text="All the occupations the character officially has/has officially had.",
    )
    main_image = models.ForeignKey(
        "images.Image",
        on_delete=models.SET_NULL,
        null=True,
        help_text="An image that illustrates the character. Something like what you'd see as the image for a character in MAL or AniList.",
    )
    
    def __str__(self) -> str:
        return self.name
