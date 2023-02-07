from django.conf import settings

from django_bunny_storage.storage import BunnyStorage


class Storage(BunnyStorage):

    def url(self, name: str) -> str:
        return settings.MEDIA_URL + name
