from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)

from django.utils.translation import gettext_lazy

from apps.user.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=120,
                              unique=True,
                              verbose_name=gettext_lazy("Email address"))

    username = models.CharField(max_length=30,
                                unique=True,
                                verbose_name=gettext_lazy("Username"))

    first_name = models.CharField(max_length=50,
                                  verbose_name=gettext_lazy("First name"))

    last_name = models.CharField(max_length=50,
                                 verbose_name=gettext_lazy("Last name"))

    phone = models.CharField(max_length=75, blank=True, null=True)


    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"  # Default filed for logining purposes

    REQUIRED_FIELDS = ["email", 'first_name', 'last_name']  # Required f. for console command 'createsuperuser'

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
