import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from characters.models import Character

from webhooks.models import Webhook

from utils.webhooks import event


@receiver(post_save, sender=Character)
def on_character_update_webhook(sender, instance, created, **kwargs):
    event(
        Webhook.Event.ON_CHARACTER_CREATE if created else Webhook.Event.ON_CHARACTER_UPDATE,
        instance,
    )


@receiver(post_delete, sender=Character)
def on_character_delete_webhook(sender, instance, **kwargs):
    event(Webhook.Event.ON_CHARACTER_DELETE, instance)
