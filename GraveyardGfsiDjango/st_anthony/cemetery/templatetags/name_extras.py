from django import template

register = template.Library()


@register.filter
def middle_name(value):
    """Dot a bare initial ("A" -> "A."); leave "A." and full names ("JOSEPH") as they are."""
    if not value:
        return ''
    value = str(value).strip()
    return f'{value}.' if len(value) == 1 and value.isalpha() else value
