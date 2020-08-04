from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The specified username must be set')

        if not password:
            raise ValueError('The specified password must be set')

        extra_fields.setdefault('first_name', None)
        extra_fields.setdefault('last_name', None)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
