from django.urls import path  # Added
from apps.todo.views import get_all_tasks


urlpatterns = [
    path("", get_all_tasks),
]
