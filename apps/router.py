from django.urls import path, include  # Added
from apps.todo.views import home_page  # Addedclear

urlpatterns = [
    path("", home_page),
    path("tasks/", include("apps.todo.urls")),
]
