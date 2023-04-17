import os

from django import template

import dotenv

dotenv.load_dotenv()


register = template.Library()


@register.filter
def envvar(value):
    return os.getenv(value)
