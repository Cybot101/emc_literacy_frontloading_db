from django import template

register = template.Library()

@register.filter
def get_by_index(list, i):
    if i < len(list):
        return list[i]
    else:
        return ''