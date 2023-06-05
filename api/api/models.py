from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class SharedResourceToken(models.Model):
    token = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r"^[\w-]{,50}$",
                message="Token must be 50 characters long and URL safe.",
                code="invalid_token",
            ),
        ],
        db_index=True
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    resource = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiry_date = timezone.now() + timezone.timedelta(days=30)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.token
