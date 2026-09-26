from django import template

register = template.Library()

GENDER_MAP = {
    'F': 'Female',
    'M': 'Male',
    'O': 'Other',
}

@register.filter
def gender_code(value):
    return GENDER_MAP.get(value, value)