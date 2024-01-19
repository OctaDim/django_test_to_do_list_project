from django.urls import path  # Added

from apps.api.views import TasksApiViews
# from apps.api.views import (get_all_tasks_response,
#                             create_new_task_response, )



app_name = "api"

urlpatterns = [
    path("tasks/", TasksApiViews.as_view(), name="")
    # path("all_tasks", get_all_tasks_response, name="get-all-tasks-response"),
    # path("create_task", create_new_task_response, name="create_new_task_response"),
]
