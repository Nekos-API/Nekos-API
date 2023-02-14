from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework_json_api import serializers

from oauth2_provider.generators import generate_client_secret

from .models import Application


class TimestampsSerializer(serializers.Serializer):
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class ClientIdSerializer(serializers.Serializer):
    """
    Serializes only the application's client_id field. This is used when the
    client secret has already been hashed and only the client ID can be seen.
    """

    clientId = serializers.CharField(source="client_id")


class CredentialsSerializer(ClientIdSerializer):
    """
    Serializes both client_id and client_secret. This serializer is only used
    when the aplication is first serialized (on create).
    """

    clientSecret = serializers.CharField(source="client_secret")


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "name",
            "description",
            "icon",
            "credentials",
            "redirect_uris",
            "client_type",
            "authorization_grant_type",
            "skip_authorization",
            "timestamps",
        ]
        extra_kwargs = {
            "icon": {"read_only": True},
            "skip_authorization": {"read_only": True},
            "redirect_uris": {"required": True},
            "name": {"required": True},
        }

    client_type = serializers.ChoiceField(choices=Application.CLIENT_TYPES)

    # Allow only authorization-code applications
    authorization_grant_type = serializers.ChoiceField(
        choices=(("authorization-code", "Authorization code"),), required=True
    )

    credentials = ClientIdSerializer(source="*", read_only=True)
    timestamps = TimestampsSerializer(source="*", read_only=True)

    def create(self, validated_data):
        """
        Creates an unsaved instance from the serializer's data. You need to
        call `.save()` after getting the client secret since it will be hashed
        afterwards.
        """
        raise_errors_on_nested_writes("create", self, validated_data)

        ModelClass = self.Meta.model

        validated_data.update({"client_secret": generate_client_secret()})

        try:
            instance = ModelClass(**validated_data)
        except TypeError:
            msg = (
                "Got a `TypeError` when calling `%s.%s.create()`. "
                "This may be because you have a writable field on the "
                "serializer class that is not a valid argument to "
                "`%s.%s.create()`. You may need to make the field "
                "read-only, or override the %s.create() method to handle "
                "this correctly."
                % (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                )
            )
            raise TypeError(msg)

        return instance


class ApplicationWithSecretSerializer(ApplicationSerializer):
    credentials = CredentialsSerializer(source="*", read_only=True)
