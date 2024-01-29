from django.contrib.auth.models import BaseUserManager  # Added

from django.core.validators import (ValidationError,  # Added
                                    validate_email)

from django.utils.translation import gettext_lazy  # Added

from apps.api.error_messages import (EMAIL_REQUIRED_MESSAGE,
                                     FIRST_NAME_REQUIRED_MESSAGE,
                                     LAST_NAME_REQUIRED_MESSAGE,
                                     NOT_IS_STAFF_ERROR,
                                     NOT_IS_SUPERUSER_ERROR,
                                     INVALID_EMAIL_ERROR, )


class CustomUserManager(BaseUserManager):  # class CustomUserManager(CustomUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError as error:
            raise ValueError(
                gettext_lazy(INVALID_EMAIL_ERROR(error.message)))

    def create_user(self, email, first_name, last_name, password, **extra_fields):

        if email:
            email = self.normalize_email(email=email)
            self.email_validator(email=email)
        else:
            raise ValueError(gettext_lazy(EMAIL_REQUIRED_MESSAGE))

        if not first_name:
            raise ValueError(gettext_lazy(FIRST_NAME_REQUIRED_MESSAGE))

        if not last_name:
            raise ValueError(gettext_lazy(LAST_NAME_REQUIRED_MESSAGE))

        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          password=password,
                          **extra_fields)

        user.save(using=self._db)
        return user

    def create_super_user(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if not extra_fields.get("is_staff"):
            raise ValueError(gettext_lazy(NOT_IS_STAFF_ERROR))

        if not extra_fields.get("is_superuser"):
            raise ValueError(gettext_lazy(NOT_IS_SUPERUSER_ERROR))

        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          password=password,
                          **extra_fields)

        user.save(using=self._db)
        return user