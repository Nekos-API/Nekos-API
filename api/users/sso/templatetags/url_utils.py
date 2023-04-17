from urllib.parse import urlparse

from django import template


register = template.Library()


@register.filter
def netloc(value):
    return urlparse(value).netloc
