from django.urls import path  # Added
from apps.todo.views import (get_all_tasks,
                             create_new_task,
                             update_task_by_id,
                             get_task_info_by_task_id,
                             delete_task,
                             )  # Added

app_name = "tasks"

urlpatterns = [
    path("", get_all_tasks, name="all-tasks"),
    path("create/", create_new_task, name="create-task"),
    path("<int:task_id>/", get_task_info_by_task_id, name="get-task"),
    path("update/<int:task_id>/", update_task_by_id, name="update-task"),
    path("delete/<int:task_id>", delete_task, name="delete-task"),
    # int: parameter type (not id !!!), task_id = views parameter name task_id
]
