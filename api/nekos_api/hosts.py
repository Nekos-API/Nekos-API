import os

from django.conf import settings
from django_hosts import patterns, host

if settings.DEBUG:
    host_patterns = patterns(
        "",
        host(rf"api.{os.getenv('BACKEND_BASE_DOMAIN')}", "nekos_api.urls", name="api"),
        host(rf"sso.{os.getenv('BACKEND_BASE_DOMAIN')}", "users.sso.urls", name="sso"),
    )
else:
    host_patterns = patterns(
        "",
        host(rf"^api\.{os.getenv('BACKEND_BASE_DOMAIN')}$", "api.urls", name="api"),
        host(rf"^sso\.{os.getenv('BACKEND_BASE_DOMAIN')}$", "users.sso.urls", name="sso"),
        host(rf"^admin\.{os.getenv('BACKEND_BASE_DOMAIN')}$", "nekos_api.urls", name="admin"),
    )
