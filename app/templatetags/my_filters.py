# yourapp/templatetags/my_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Usage: {{ my_dict|get_item:my_key }} returns dictionary[my_key]"""
    return dictionary.get(key)
