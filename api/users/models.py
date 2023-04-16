import uuid
import secrets

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

from validators.domain import domain

from django_resized import ResizedImageField

from dynamic_filenames import FilePattern

import dns.resolver

import requests

# Create your models here.


class User(AbstractUser):
    """
    User model.
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, null=False
    )

    nickname = models.CharField(max_length=50, null=True, blank=True)

    biography = models.CharField(max_length=500, null=True, blank=True)

    avatar_image = ResizedImageField(
        size=[512, 512],
        crop=["middle", "center"],
        upload_to=FilePattern(
            filename_pattern="uploads/user/avatar/{uuid:base32}{ext}"
        ),
        blank=True,
        null=True,
    )

    liked_images = models.ManyToManyField(
        "images.Image", blank=True, related_name="liked_by"
    )
    saved_images = models.ManyToManyField(
        "images.Image", blank=True, related_name="saved_by"
    )

    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    followed_characters = models.ManyToManyField(
        "characters.Character", related_name="followers"
    )
    followed_categories = models.ManyToManyField(
        "categories.Category", related_name="followers"
    )
    followed_artists = models.ManyToManyField(
        "artists.Artist", related_name="followers"
    )
    followed_lists = models.ManyToManyField("lists.List", related_name="followers")


class DiscordUser(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True, unique=True)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(
        User, unique=True, related_name="discord", on_delete=models.CASCADE
    )

    access_token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=256)


class GoogleUser(models.Model):
    id = models.CharField(
        primary_key=True, null=False, blank=False, unique=True, max_length=256
    )
    email = models.EmailField(null=False, blank=False, unique=True)
    user = models.OneToOneField(
        User, unique=True, related_name="google", on_delete=models.CASCADE
    )


class GitHubUser(models.Model):
    class Meta:
        verbose_name = "GitHub User"
        verbose_name_plural = "GitHub Users"

    id = models.PositiveBigIntegerField(
        primary_key=True, unique=True, blank=False, null=False
    )
    email = models.EmailField(null=False, blank=False)
    user = models.OneToOneField(User, related_name="github", on_delete=models.CASCADE)


class Domain(models.Model):
    def validate_domain(value) -> None:
        if domain(value) != True:
            raise ValidationError("Invalid domain name.")

    def generate_token() -> str:
        return secrets.token_urlsafe(32)

    class VerificationMethod(models.TextChoices):
        DNS = "dns"
        FILE = "file"

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    name = models.CharField(max_length=254, validators=[validate_domain], unique=True)
    user = models.ForeignKey(
        "users.User", related_name="domains", on_delete=models.CASCADE
    )

    verification_token = models.CharField(
        default=generate_token, editable=False, null=False, blank=False, max_length=43
    )
    verification_method = models.CharField(
        choices=VerificationMethod.choices,
        default=VerificationMethod.DNS,
        null=False,
        blank=False,
        max_length=5,
    )

    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def verify(self):
        """
        Try to verify the domain
        """
        if self.verification_method == Domain.VerificationMethod.DNS:
            answer = dns.resolver.resolve(self.name, "TXT")

            self.verified = False

            for record in answer:
                record = record.to_text()

                if record == f'"nekosapi-verification={self.verification_token}"':
                    self.verified = True
                    break

            self.save()

        elif self.verification_method == Domain.VerificationMethod.FILE:
            self.verified = False
            r = requests.get(f"https://{self.name}/nekosapi-verify.txt", timeout=5)

            if r.status_code not in range(200, 300):
                self.save()
                return self.verified

            try:
                if r.text == f"nekosapi-verification={self.verification_token}":
                    self.verified = True
                    self.save()
            except:
                self.verified = False
                self.save()

        return self.verified
