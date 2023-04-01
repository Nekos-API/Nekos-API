from django.conf import settings

from django_bunny_storage.storage import BunnyStorage

import requests


class Storage(BunnyStorage):

    def url(self, name: str) -> str:
        return settings.MEDIA_URL + name

    def size(self, name: str) -> int:
        return int(requests.head(self.url(name)).headers.get("Content-Length", 0))
