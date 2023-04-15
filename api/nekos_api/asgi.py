import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application

from nekos_api.middleware import WebSocketHostMiddleware

from webhooks import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nekos_api.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": WebSocketHostMiddleware(
            SessionMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
        ),
    }
)
