from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    
    return dictionary.get(key, [])


@register.filter
def index(value, i):
    """Returns the i-th element from the list or '-' if out of range"""
    try:
        return value[i]
    except (IndexError, TypeError):
        return "-"
    
@register.filter
def custom_range(value):
    """Returns a range object from 0 to value."""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return []