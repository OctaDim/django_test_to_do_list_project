from django.contrib.auth.backends import ModelBackend  # Added
from django.contrib.auth.backends import UserModel  # Added
# from django.shortcuts import get_object_or_404
# from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy
from apps.api.error_messages import (EMAIL_OR_USERNAME_REQUIRED_MESSAGE,
                                     PASSWORD_REQUIRED_MESSAGE,
                                     USER_NOT_FOUND_MESSAGE)


class CustomEmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get("username")  # Get username with email entered on purpose or by mistake

        if username is None:
            gettext_lazy(EMAIL_OR_USERNAME_REQUIRED_MESSAGE)
            return None

        if password is None:
            gettext_lazy(PASSWORD_REQUIRED_MESSAGE)
            return None

        try:
            user = UserModel.objects.get(email=username)  # Get user by email entered as username
        except UserModel.DoesNotExist:
            gettext_lazy(USER_NOT_FOUND_MESSAGE(username))

            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
