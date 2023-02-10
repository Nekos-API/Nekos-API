from django.conf import settings
from django_hosts import patterns, host

if settings.DEBUG:
    host_patterns = patterns(
        "",
        host(r"localhost", "nekos_api.urls", name="api"),
    )
else:
    host_patterns = patterns(
        "",
        host(r"^api\.nekosapi\.com$", "api.urls_api", name="api"),
        host(r"^admin\.nekosapi\.com$", "nekos_api.urls", name="admin"),
    )
