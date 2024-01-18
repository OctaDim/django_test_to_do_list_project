from django.urls import path, include  # Added

from apps.user.views import login_existing_user, register_new_user

app_name = "user"

urlpatterns = [
    path("login/", login_existing_user, name="login-existing-user"),
    path("register/", register_new_user, name="register_new_user"),
]
