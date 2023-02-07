from django.conf import settings
from django_hosts import patterns, host

if settings.DEBUG:
    host_patterns = patterns(
        "",
        host(r"localhost", "nekos_api.urls", name="api"),
        host(r"127\.0\.0\.1", "api.urls_sso", name="sso"),
    )
else:
    host_patterns = patterns(
        "",
        host(r"api\.nekosapi\.com", "api.urls_api", name="api"),
        host(r"sso\.nekosapi\.com", "api.urls_sso", name="sso"),
        host(r"admin\.nekosapi\.com", "nekos_api.urls", name="admin"),
    )
