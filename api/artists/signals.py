from asgiref.sync import async_to_sync

import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from channels.layers import get_channel_layer

from artists.models import Artist


channel_layer = get_channel_layer()


@receiver(post_save, sender=Artist)
def on_artist_update_webhook(sender, instance, created, **kwargs):
    async_to_sync(channel_layer.group_send)(
        "events",
        {
            "type": "event",
            "data": {
                "event": f"on-artist-{'create' if created else 'update'}",
                "data": {
                    "id": str(instance.pk),
                    "type": "artist",
                    "url": f"https://api.nekosapi.com/v2/artists/{instance.pk}",
                },
            },
        },
    )

@receiver(post_delete, sender=Artist)
def on_artist_delete_webhook(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(
        "events",
        {
            "type": "event",
            "data": {
                "event": "on-artist-delete",
                "data": {
                    "id": str(instance.pk),
                    "type": "artist",
                    "url": None,
                },
            },
        },
    )


