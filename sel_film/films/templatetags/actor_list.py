from django import template

register = template.Library()


@register.filter(name='actor_list')
def actor_list(obj_list):
    s = ' '.join(f'{actor.first_name} {actor.last_name},' for actor in obj_list)
    return s[:len(s)-1]

