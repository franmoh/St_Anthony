import os

from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def versioned_static(path):
    """static() URL plus ?v=<file mtime>, so browsers fetch the file again
    whenever it is rebuilt instead of reusing a stale cached copy."""
    url = static(path)
    found = finders.find(path)
    if found:
        url += f'?v={int(os.path.getmtime(found))}'
    return url
