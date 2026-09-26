from django import template
from django.utils.html import format_html

from cemetery.spam_guard import STAMP_FIELD, TRAP_FIELD, make_stamp

register = template.Library()


@register.simple_tag
def spam_guard():
    """Hidden trap field + signed timestamp; checked by spam_guard.check_submission()."""
    return format_html(
        '<div aria-hidden="true" style="position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden">'
        '<label>Leave this field empty <input type="text" name="{}" tabindex="-1" autocomplete="off"></label>'
        '</div>'
        '<input type="hidden" name="{}" value="{}">',
        TRAP_FIELD, STAMP_FIELD, make_stamp(),
    )
