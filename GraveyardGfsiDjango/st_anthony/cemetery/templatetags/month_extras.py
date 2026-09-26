from django import template
import calendar

register = template.Library()

@register.filter
def month_name(month_number):
    if not isinstance(month_number, int) or not 1 <= month_number <= 12:
        return ''
    return calendar.month_name[month_number]
