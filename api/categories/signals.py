import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from categories.models import Category

from webhooks.models import Webhook

from utils.webhooks import event


@receiver(post_save, sender=Category)
def on_category_update_webhook(sender, instance, created, **kwargs):
    event(
        Webhook.Event.ON_CATEGORY_CREATE if created else Webhook.Event.ON_CATEGORY_UPDATE,
        instance,
    )


@receiver(post_delete, sender=Category)
def on_category_delete_webhook(sender, instance, **kwargs):
    event(Webhook.Event.ON_CATEGORY_DELETE, instance)
