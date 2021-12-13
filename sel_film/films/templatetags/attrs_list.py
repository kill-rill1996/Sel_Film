from django import template

register = template.Library()


@register.filter(name='object_list')
def object_list(obj_list):
    return ', '.join([obj.title for obj in obj_list])


