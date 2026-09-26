from django import template

register = template.Library()

STATUS_MAP = {
    'FB': 'Full Body',
    'L': 'Living',
    'S': 'Spirit',
    'I': 'Infant',
    'O': 'Available',
    'A': 'Ashes',
    'U': 'Unknown',
}

@register.filter
def status_code(value):
    return STATUS_MAP.get(value, value)   