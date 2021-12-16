from django import template

register = template.Library()


@register.filter(name='truncate_title')
def truncate_title(title):
    words = title.split()
    if any([len(word) > 11 for word in words]):
        return title[:9] + '...'
    return title
