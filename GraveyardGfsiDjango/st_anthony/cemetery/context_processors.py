from .decorators import is_admin_user


def admin_flags(request):
    """`is_admin` in every template, using the same test as @admin_required."""
    return {'is_admin': is_admin_user(request.user)}
