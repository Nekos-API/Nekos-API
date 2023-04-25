from asgiref.sync import async_to_sync

from django.urls import reverse
from django.db.models import Model

from channels.layers import get_channel_layer

# grequests must be kept above requests
import grequests
import requests

from webhooks.models import Webhook


channel_layer = get_channel_layer()


def event(event_type: Webhook.Event, instance: Model, **kwargs):
    # Send a message to all clients connected to the websocket API.
    async_to_sync(channel_layer.group_send)(
        "events",
        {
            "type": "event",
            "data": {
                "type": "event",
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

    webhooks = Webhook.objects.get(events__contains=[event_type])

    rs = []

    for webhook in webhooks:
        rs.append(grequests.get(webhook.url, timeout=5))

    # Make all requests asynchronously
    responses = grequests.map(rs, size=20)

    i = 0
    for response in responses:
        try:
            if r.text == f"nekosapi-verify={webhook.verification_key}":
                pass

        except:
            pass

        i += 1
