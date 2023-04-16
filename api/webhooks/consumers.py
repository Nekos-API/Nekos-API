from enum import Enum
from asgiref.sync import async_to_sync

import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from schema import Schema, And, Use, Optional, SchemaError


class EventConsumer(AsyncJsonWebsocketConsumer):
    groups = ["events"]

    async def connect(self) -> None:
        await self.accept()
        self.scope["session"]["events"] = []

    async def disconnect(self, code: int) -> None:
        pass

    async def receive_json(self, content) -> None:
        from webhooks.models import Webhook

        subscription_schema = {
            "event": Use(Webhook.Event),
            "subscribe": bool,
            Optional("data"): {
                "type": Use(str, lambda t: t in ("image",)),
                "id": Use(str),
            },
        }

        try:
            content = Schema(subscription_schema).validate(content)

            if content["subscription"]:
                subscription = {
                    "event": content["event"],
                    "data": content.get("data", None),
                }

                if subscription not in self.scope["session"]["events"]:
                    self.scope["session"]["events"].append(subscription)

                else:
                    await self.send_json(
                        {
                            "event": "existent-subscription-error",
                            "data": {
                                "message": "You have already subscribed to this event."
                            },
                        },
                    )

            else:
                subscription = {
                    "event": content["event"],
                    "data": content.get("data", None),
                }

                if subscription in self.scope["session"]["events"]:
                    self.scope["session"]["events"].remove(subscription)

                else:
                    await self.send_json(
                        {
                            "event": "unexistent-subscription-error",
                            "data": {
                                "message": "You are not subscribed to this event."
                            },
                        },
                    )

        except SchemaError:
            await self.send_json(
                {
                    "event": "schema-error",
                    "data": {
                        "message": "The received message is not valid or it has an invalid parameter."
                    },
                }
            )

    async def event(self, data: dict) -> None:
        data = data["data"]

        event_name = data["event"]

        subscriptions = [
            s for s in self.scope["session"]["events"] if s["event"].value == event_name
        ]

        notify = False

        if len(subscriptions) > 0:
            for subscription in subscriptions:
                if subscription["data"] is not None:
                    if data["data"]["id"] == subscription["data"]["id"]:
                        notify = True
                        break
                else:
                    notify = True
                    break

        if notify:
            await self.send_json(data)
