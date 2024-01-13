from django.urls import path, include  # Added
from apps.todo.views import home_page  # Addedclear

app_name = "router"

urlpatterns = [
    path("", home_page, name="home"),
    path("tasks/", include("apps.todo.urls")),
]
