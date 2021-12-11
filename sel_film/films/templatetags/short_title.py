from django import template

register = template.Library()


@register.filter(name='truncate_title')
def truncate_title(title):
    words = title.split()
    if len(words) == 1 and len(words[0]) > 11:
        return words[0][:10] + '...'
    return title
