from django.contrib.auth.forms import (AuthenticationForm,
                                       UserCreationForm)  # Added
from django import forms
from django.forms.widgets import TextInput, PasswordInput  # Added
from django.contrib.auth.models import User  # Added
# from django.contrib.auth.forms import UsernameField  # Added for class default user and pass fields parameters

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={"autofocus": True}), )
    password = forms.CharField(label="Password", widget=PasswordInput(), strip=True)

    # username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))  # By default, in AuthenticationForm
    # password = forms.CharField(label="Password",
    #                            strip=False,
    #                            widget=forms.PasswordInput(
    #                                attrs={"autocomplete": "current-password"}), )  # By default, in AuthenticationForm


class CreateNewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name",
                  "last_name",
                  "username",
                  "email",
                  "password1",  # Password (first entered). By default, will be validated by AUTH_PASSWORD_VALIDATORS from main settings
                  "password2",  # Password second (confirmation). By default, will be validated by AUTH_PASSWORD_VALIDATORS from main settings
                  ]
