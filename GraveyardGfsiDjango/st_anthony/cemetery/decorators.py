from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    """Restrict a view to active, unlocked admin users.

    - Anonymous users are redirected to LOGIN_URL with a ?next= back-link.
    - Authenticated users who are not an active, unlocked admin receive a 403.

    'Admin' maps to Users.is_staff (role == Users.Role.ADMIN). The auth backend
    already blocks inactive/locked accounts at login, but get_user() does not
    re-check on each request, so an account deactivated or locked mid-session is
    rejected here too.
    """

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not (user.is_active and not user.is_locked and user.is_staff):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped
