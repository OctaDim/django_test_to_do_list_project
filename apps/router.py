from django.urls import path,include  # Added
from apps.todo.views import hello_world  # Addedclear

urlpatterns = [
    path("", hello_world),
    # path("tasks/", include("apps.todo.urls")),
]
