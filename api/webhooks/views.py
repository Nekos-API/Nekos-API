from django.utils.decorators import method_decorator

from rest_framework import permissions
from rest_framework_json_api import views

from django_ratelimit.decorators import ratelimit

from webhooks.models import Webhook
from webhooks.serializers import WebhookSerializer

# Create your views here.


@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="list")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="retrieve")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="retrieve_related")
@method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="update")
# @method_decorator(ratelimit(group="api", key="ip", rate="3/s"), name="create")
class WebhookViewSet(views.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WebhookSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Webhook.objects.all()
        return Webhook.objects.filter(user=self.request.user)
