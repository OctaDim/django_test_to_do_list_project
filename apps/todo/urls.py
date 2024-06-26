from django.urls import path  # Added
from apps.todo.views import (get_all_tasks,
                             create_new_task,
                             update_task_by_id,
                             get_task_by_task_id,
                             delete_task,
                             get_all_subtasks_by_creator,
                             get_subtask_by_id,
                             update_subtask_by_subtask_id,
                             create_new_subtask,
                             delete_subtask_by_id
                             )  # Added

app_name = "tasks"

urlpatterns = [
    path("", get_all_tasks, name="get-all-tasks"),
    path("<int:task_id>/", get_task_by_task_id, name="get-task-by-id"),
    path("create/", create_new_task, name="create-task"),
    path("update/<int:task_id>/", update_task_by_id, name="update-task"),
    path("delete/<int:task_id>/", delete_task, name="delete-task"),

    path("subtasks", get_all_subtasks_by_creator, name="get-all-subtasks-by-creator"),
    path("subtask/<int:subtask_id>/", get_subtask_by_id, name="get-subtask-by-id"),
    path("subtasks/create/", create_new_subtask, name="create-new-subtask"),
    path("subtasks/update/<int:subtask_id>/", update_subtask_by_subtask_id, name="update_subtask_by_subtask_id"),
    path("subtasks/delete/<int:subtask_id>/", delete_subtask_by_id, name="delete-subtask-by-id")

]
