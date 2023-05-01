from django import template

register = template.Library()


@register.filter
def replace(value, arg):
    return value.replace(arg.split(',')[0], arg.split(',')[1])
