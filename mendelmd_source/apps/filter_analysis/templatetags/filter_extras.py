from django import template
#from django.conf import settings

register = template.Library()

def cut(variant):
    links = variant.cln_omim.split('|')
    new_links = []
    for link in links:
        if link == 'http://www.ncbi.nlm.nih.gov/sites/varvu?gene':
            link = "%s=%s&rs=%s" % (link, variant.gene_name, variant.variant_id)
        new_links.append(link)
        
    return new_links


def cleanstr(value):
    """Removes all values of arg from the given string"""
    return value.replace('_', ' ')

@register.filter
def adjust_for_pagination(page, current):
    if (current - page) in [-1,-2,1,2]:
        return True
    else: 
        return False
    
#    if (current - page) <= -2:
#        return True
#    

#
          
#    value, page = int(value), int(page)
#    adjusted_value = value + ((page - 1))
#    return adjusted_value

register.filter('adjust_for_pagination', adjust_for_pagination)
register.filter('cut', cut)
register.filter('cleanstr', cleanstr)

