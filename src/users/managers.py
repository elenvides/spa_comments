from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password

from users.constants import Role


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        password = make_password(password)
        user = self.model(email=email, username=username, password=password, **extra_fields)
        user.save(using=self._db)

        return user

    def create_user(self, email: str, username: str, password: str, **extra_fields):
        extra_fields["is_staff"] = False
        extra_fields["role"] = Role.USER

        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email: str, username: str, password: str, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["role"] = Role.ADMIN

        return self._create_user(email, username, password, **extra_fields)

