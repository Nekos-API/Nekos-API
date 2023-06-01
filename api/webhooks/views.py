from django.utils.decorators import method_decorator

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_json_api import views

from django_ratelimit.decorators import ratelimit

from webhooks.models import Webhook
from webhooks.serializers import WebhookSerializer

# Create your views here.


class WebhookViewSet(views.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WebhookSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Webhook.objects.all()
        return Webhook.objects.filter(user=self.request.user)

    def delete(self, request, pk):
        """
        Delete a webhook.
        """

        webhook = get_object_or_404(self.get_queryset().select_related("user"), pk=pk)

        webhook.delete()

        return Response(data="", status=204)


class WebhookRelationshipsView(views.RelationshipView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WebhookSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Webhook.objects.all()
        return Webhook.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.request.method != "GET":
            return [permissions.IsAdminUser]
        return []
