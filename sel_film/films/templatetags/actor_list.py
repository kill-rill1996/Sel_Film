from django import template

register = template.Library()


@register.filter(name='actor_list')
def actor_list(obj_list):
    return obj_list[:4] + ['...'] if len(obj_list) > 4 else obj_list

