import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from artists.models import Artist

from webhooks.models import Webhook

from utils.webhooks import event


@receiver(post_save, sender=Artist)
def on_artist_update_webhook(sender, instance, created, **kwargs):
    event(
        Webhook.Event.ON_ARTIST_CREATE if created else Webhook.Event.ON_ARTIST_UPDATE,
        instance,
    )


@receiver(post_delete, sender=Artist)
def on_artist_delete_webhook(sender, instance, **kwargs):
    event(Webhook.Event.ON_ARTIST_DELETE, instance)
