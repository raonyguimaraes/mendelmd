from django import template
register = template.Library()

@register.simple_tag
def dictKeyLookup(the_dict, key):
   # Try to fetch from the dict, and if it's not found return an empty string.
   return the_dict.get(key, '0')


@register.filter
def adjust_for_pagination(page, current):
    if (current - page) in [-1,-2,1,2]:
        return True
    else: 
        return False
register.filter('dictKeyLookup', dictKeyLookup)
register.filter('adjust_for_pagination', adjust_for_pagination)
