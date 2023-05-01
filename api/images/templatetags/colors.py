from django import template

register = template.Library()


@register.filter
def brightness(value):
    return 0.2126 * value[0] + 0.7152 * value[1] + 0.0722 * value[2]


@register.filter
def hex(value):
    return '#{:02x}{:02x}{:02x}'. format(value[0], value[1], value[2])
