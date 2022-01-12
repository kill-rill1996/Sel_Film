from django import template

register = template.Library()


@register.filter(name='to_int')
def to_int(rating):
    return int(float(rating) * 10)

