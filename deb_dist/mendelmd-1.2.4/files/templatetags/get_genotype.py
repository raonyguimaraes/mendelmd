from django import template

register = template.Library()


@register.filter
def get_genotype(variant):
    """Removes all values of arg from the given string"""
    genotype = variant.genotype
    if genotype == '0/0':
        return('(%s;%s)' % (variant.ref, variant.ref))
    elif genotype == '0/1':
        return('(%s;%s)' % (variant.ref, variant.alt))
    elif genotype == '1/0':
        return('(%s;%s)' % (variant.alt, variant.ref))
    elif genotype == '1/1':
        return('(%s;%s)' % (variant.alt, variant.alt))
    else:
        return ('ref:%s, alt:%s, genotype:%s' % (variant.ref, variant.alt, variant.genotype))
