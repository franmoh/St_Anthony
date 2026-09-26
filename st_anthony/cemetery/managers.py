from django.contrib.auth.base_user import BaseUserManager


class UsersManager(BaseUserManager):

    def get_by_natural_key(self, username):
        return self.get(username=username)

    def create_user(self, username, password=None, created_by=1, **extra_fields):
        if not username:
            raise ValueError('Username is required')

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_locked', False)
        extra_fields.setdefault('force_password_change', False)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)

        user.created_by_id = created_by

        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'Admin')
        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'User')

        return self.create_user(username, password, created_by=1, **extra_fields)