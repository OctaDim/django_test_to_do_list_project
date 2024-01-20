from django.urls import path  # Added

# views via functions (samples)
from apps.api.views.views_functions import (get_all_tasks_response,
                                            create_new_task_response, )
# views via ApiViews Classes (samples)
from apps.api.views.views_api_views import TasksApiViews

# views via GenericViews Classes (samples)
from apps.api.views.views_generic_views import TaskDetailGenericViews


app_name = "api"

urlpatterns = [
    # views via ViewSet (samples)
    # path(),

    # views via GenericViews (samples)
    path("generic/task/<int:task_id>", TaskDetailGenericViews.as_view(), name="get-task-by-id-generic"),

    # views via ApiViews classes (samples)
    path("api_views/tasks/", TasksApiViews.as_view(), name="tasks-api-views"),

    # views via functions (samples)
    path("funcs/all_tasks", get_all_tasks_response, name="get-all-tasks-function"),
    path("funcs/create_task", create_new_task_response, name="create_new_task_function"),
]
