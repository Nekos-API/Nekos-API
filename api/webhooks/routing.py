from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/events", consumers.EventConsumer.as_asgi()),
]
