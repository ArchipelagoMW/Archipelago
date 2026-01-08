from django import template

register = template.Library()


@register.filter
def levels_range(levels):
    return range(levels + 1)
