from django import template

register = template.Library()

@register.filter
def dictlookup(d, key):
    return d.get(key, '')
