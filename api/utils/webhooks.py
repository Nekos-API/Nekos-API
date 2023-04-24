from asgiref.sync import async_to_sync

from django.urls import reverse
from django.db.models import Model

from channels.layers import get_channel_layer

import requests

from webhooks.models import Webhook


channel_layer = get_channel_layer()


def event(event_type: Webhook.Event, instance: Model, **kwargs):
    async_to_sync(channel_layer.group_send)(
        "events",
        {
            "type": "event",
            "data": {
                "event": {
                    "name": event_type.value.replace("-", " ").title(),
                    "id": str(event_type.value)
                },
                "data": {
                    "id": str(instance.pk),
                    "type": instance.JSONAPIMeta.resource_name
                },
            },
        },
    )

    for webhook in Webhook.objects.select_related("user").filter(
        events__contains=[event_type]
    ):
        user = webhook.user
        domain = webhook.domain

        try:
            if domain.verified:
                requests.post(
                    webhook.url,
                    json={
                        "webhook": {"name": webhook.name, "id": str(webhook.id)},
                        "data": {
                            "event": event_type.value,
                            "resource": {
                                "type": instance.JSONAPIMeta.resource_name,
                                "id": str(instance.pk),
                            },
                        },
                        "secretKey": user.secret_key,
                    },
                )

        except AttributeError:
            pass
