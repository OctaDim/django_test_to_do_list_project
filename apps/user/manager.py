from django.contrib.auth.base_user import BaseUserManager

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.utils.translation import gettext_lazy

from apps.api.error_messages import (INVALID_EMAIL_ERROR,
                                     EMAIL_REQUIRED_MESSAGE,
                                     LAST_NAME_REQUIRED_MESSAGE,
                                     FIRST_NAME_REQUIRED_MESSAGE,
                                     NOT_IS_STAFF_ERROR,
                                     NOT_IS_SUPERUSER_ERROR,
                                     USERNAME_REQUIRED_MESSAGE,
                                     )


class UserManager(BaseUserManager):

    def email_validator(self, email):
        try:
            validate_email(email)

        except ValidationError as error:
            raise ValueError(
                gettext_lazy(INVALID_EMAIL_ERROR(error.message)))

    def create_user(self,
                    email=None,     # Named parameters extracted to check or make ops
                    username=None,  # others falling into **extra_fields
                    first_name=None,
                    last_name=None,
                    password=None,
                    **extra_fields):

        if not email:
            raise ValueError(gettext_lazy(EMAIL_REQUIRED_MESSAGE))
        else:
            email = self.normalize_email(email=email)
            # self.email_validator(email=email)

        ERROR_MESSAGE = []
        if not username:
            ERROR_MESSAGE.append(gettext_lazy(USERNAME_REQUIRED_MESSAGE))
            # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))

        if not first_name:
            ERROR_MESSAGE.append(gettext_lazy(FIRST_NAME_REQUIRED_MESSAGE))
            # raise ValueError(gettext_lazy(FIRST_NAME_REQUIRED_MESSAGE))

        if not last_name:
            ERROR_MESSAGE.append(gettext_lazy(LAST_NAME_REQUIRED_MESSAGE))
            # raise ValueError(gettext_lazy(LAST_NAME_REQUIRED_MESSAGE))

        if ERROR_MESSAGE:
            raise ValueError(", ".join(ERROR_MESSAGE))

        user = self.model(email=email,  # Named parameters extracted to check or make ops
                          username=username,
                          first_name=first_name,
                          last_name=last_name,
                          password=password,
                          **extra_fields  # Other kwarg fields, that are in not named parameters
                          )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,
                         email=None,    # Named parameters extracted to check or make ops
                         username=None, # others falling into **extra_fields
                         first_name=None,
                         last_name=None,
                         password=None,
                         # is_staff=None,
                         # is_superuser=None,
                         # is_verified=None,
                         **extra_fields):

        ERROR_MESSAGE = []

        # extra_fields.setdefault("is_staff", True)
        # extra_fields.setdefault("is_superuser", True)
        # extra_fields.setdefault("is_verified", True)


        # if not extra_fields.get("is_staff"):
        #     ERROR_MESSAGE.append(gettext_lazy(NOT_IS_STAFF_ERROR))
        #     # raise ValueError(gettext_lazy(NOT_IS_STAFF_ERROR))

        # if not extra_fields.get("is_superuser"):
        #     ERROR_MESSAGE.append(gettext_lazy(NOT_IS_SUPERUSER_ERROR))
        #     # raise ValueError(gettext_lazy(NOT_IS_SUPERUSER_ERROR))

        # if not extra_fields.get("is_verified"):
        #     ERROR_MESSAGE.append(gettext_lazy(NOT_IS_SUPERUSER_ERROR))
        #     # raise ValueError(gettext_lazy(NOT_IS_SUPERUSER_ERROR))

        if not email:
            ERROR_MESSAGE.append(gettext_lazy(EMAIL_REQUIRED_MESSAGE))
            # raise ValueError(gettext_lazy(EMAIL_REQUIRED_MESSAGE))
        else:
            email = self.normalize_email(email=email)
            # self.email_validator(email=email)

        if not username:
            ERROR_MESSAGE.append(gettext_lazy(USERNAME_REQUIRED_MESSAGE))
            # raise ValueError(gettext_lazy(USERNAME_REQUIRED_MESSAGE))

        if ERROR_MESSAGE:
            raise ValueError(ERROR_MESSAGE)

        user = self.model(email=email,  # Named parameters extracted to check or make ops
                          username=username,
                          first_name=first_name,
                          last_name=last_name,
                          password=password,
                          **extra_fields,    # Other kwarg fields, that are in not named parameters
                          )

        user.set_password(password)
        user.save(using=self._db)

        return user
