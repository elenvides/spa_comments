from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from users.constants import Role
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150, unique=True, null=False)
    username = models.CharField(max_length=30, unique=True)
    home_page = models.URLField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    role = models.PositiveSmallIntegerField(choices=[(role.value, role.name) for role in Role])

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username
