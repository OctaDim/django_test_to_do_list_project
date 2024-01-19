from django.urls import path  # Added

from apps.api.views import get_all_tasks_response

app_name = "api"

urlpatterns = [
    path("all_tasks", get_all_tasks_response, name="get-all-tasks-response")
]
