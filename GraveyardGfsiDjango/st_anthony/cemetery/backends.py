from django.contrib.auth.backends import BaseBackend
from .models import Users


class UsersAuthBackend(BaseBackend):
    @staticmethod
    def _as_bool(value):
        # MySQL BIT(1) may be returned as bytes (b"\x00"/b"\x01").
        if isinstance(value, (bytes, bytearray, memoryview)):
            return any(value)
        return bool(value)

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return None

        is_active = self._as_bool(user.is_active)
        is_locked = self._as_bool(user.is_locked)
        if not is_active or is_locked:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
