from django.urls import path

from .views import WebhookViewSet

urlpatterns = [
    path(
        "webhooks", WebhookViewSet.as_view({"get": "list", "post": "create"}), name="webhook"
    ),
    path(
        "webhooks/<uuid:pk>",
        WebhookViewSet.as_view({"get": "retrieve", "patch": "update", "delete": "delete"}),
        name="webhook-detail",
    ),
    path(
        "webhooks/<uuid:pk>/<related_field>",
        WebhookViewSet.as_view({"get": "retrieve_related"}),
        name="webhook-related",
    ),
]
