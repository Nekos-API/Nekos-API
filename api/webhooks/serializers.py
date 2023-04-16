from rest_framework_json_api import serializers, relations

from webhooks.models import Webhook


class WebhookSerializer(serializers.HyperlinkedModelSerializer):
    included_serializers = {"user": "users.serializers.UserPublicSerializer"}

    class Meta:
        model = Webhook
        fields = [
            "name",
            "events",
            "urls",
            "user",
        ]

    def validate(self, attrs):
        """
        Set the uploader to the user itself.
        """

        attrs["user"] = self.context["request"].user
        return attrs

    user = relations.ResourceRelatedField(
        read_only=True,
        related_link_view_name="webhook-related",
        self_link_view_name="webhook-relationships",
    )
