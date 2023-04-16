from rest_framework_json_api import serializers

from webhooks.models import Webhook


class WebhookSerializer(serializers.ModelSerializer):
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
