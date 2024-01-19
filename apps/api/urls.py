from django.urls import path  # Added

# views via functions (samples)
from apps.api.views.views_functions import (get_all_tasks_response,
                                            create_new_task_response, )

# views via api views classes (samples)
from apps.api.views.views_api_views import TasksApiViews

app_name = "api"

urlpatterns = [
    # views via view set (samples)
    # path(),

    # views via generic views (samples)
    # path(),

    # views via api views classes (samples)
    path("api_views/tasks/", TasksApiViews.as_view(), name=""),

    # views via functions (samples)
    path("funcs/all_tasks", get_all_tasks_response, name="get-all-tasks-response"),
    path("funcs/create_task", create_new_task_response, name="create_new_task_response"),
]
