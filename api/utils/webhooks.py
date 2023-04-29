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
                    "id": str(event_type.value),
                },
                "data": {
                    "id": str(instance.pk),
                    "type": instance.JSONAPIMeta.resource_name,
                },
            },
        },
    )

    webhooks = Webhook.objects.filter(events__contains=[event_type])

    get_rs = []

    for webhook in webhooks:
        get_rs.append(grequests.get(webhook.url, timeout=5))

    # Make all requests asynchronously
    responses = grequests.map(get_rs, size=20)

    post_rs = []

    i = 0
    for response in responses:
        webhook = webhooks[i]
        try:
            if r.text == f"nekosapi-verify={webhook.verification_key}":
                post_rs.append(
                    grequests.post(
                        webhooks[i].url,
                        timeout=5,
                        json={
                            "webhook": {"name": webhook.name, "id": webhook.id, "url": webhook.url},
                            "data": {
                                "event": str(event_type.value),
                                "resource": {
                                    "type": instance.JSONAPIMeta.resource_name,
                                    "id": str(instance.pk)
                                },
                            },
                            "secretKey": webhook.user.secret_key,
                        },
                    )
                )

        except:
            pass

        i += 1

    # Make all requests asynchronously
    grequests.map(post_rs, size=20)
