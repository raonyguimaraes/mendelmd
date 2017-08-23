from django import template

register = template.Library()


@register.filter
def paginator(context, adjacent_pages=2):
    current_page = context['page_obj'].number
    number_of_pages = context['paginator'].num_pages
    page_obj = context['page_obj']
    paginator = context['paginator']
    startPage = max(current_page - adjacent_pages, 1)
    endPage = current_page + adjacent_pages + 1
    if endPage > number_of_pages: endPage = number_of_pages + 1
    page_numbers = [n for n in range(startPage, endPage) \
        if 0 < n <= number_of_pages]

    return {
        'page_obj': page_obj,
        'paginator': paginator,
        'page': current_page,
        'pages': number_of_pages,
        'page_numbers': page_numbers,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'show_first': 1 != current_page,
        'show_last': number_of_pages != current_page,
    }

register.inclusion_tag('list.html', takes_context=True)(paginator)