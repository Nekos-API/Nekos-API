from asgiref.sync import async_to_sync

import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from channels.layers import get_channel_layer

from images.models import Image


channel_layer = get_channel_layer()


@receiver(post_save, sender=Image)
def on_image_update_webhook(sender, instance, created, **kwargs):
    async_to_sync(channel_layer.group_send)(
        "events",
        {
            "type": "event",
            "data": {
                "event": f"on-image-{'create' if created else 'update'}",
                "data": {
                    "id": str(instance.pk),
                    "type": "image",
                    "url": f"https://api.nekosapi.com/v2/images/{instance.pk}",
                },
            },
        },
    )

@receiver(post_delete, sender=Image)
def on_image_delete_webhook(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(
        "events",
        {
            "type": "event",
            "data": {
                "event": "on-image-delete",
                "data": {
                    "id": str(instance.pk),
                    "type": "image",
                    "url": None,
                },
            },
        },
    )


