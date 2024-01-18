from django.urls import path, include  # Added

from apps.user.views import (login_existing_user,
                             register_new_user,
                             user_profile_info,
                             logout_user,
                             )

app_name = "user"

urlpatterns = [
    path("login/", login_existing_user, name="login-existing-user"),
    path("register/", register_new_user, name="register-new-user"),
    path("info", user_profile_info, name="user-profile-info"),
    path("logout/", logout_user, name="logout-user"),
]
