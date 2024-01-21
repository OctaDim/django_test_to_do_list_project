from django.urls import path  # Added
from rest_framework.routers import DefaultRouter  # Added, for ModelViewSet

# views via functions (samples)
from apps.api.views.views_functions import (get_all_tasks,
                                            create_new_task, )
# views via ApiViews Classes (samples)
from apps.api.views.views_api_views import TasksApiViews

# views via GenericViews Classes (samples)
from apps.api.views.views_generic_views import TaskDetailGenericViews

# views via ModelViewSet Classes (samples)
from apps.api.views.views_model_view_set import (StatusViewSet,
                                                 CategoryViewSet)

app_name = "api"

urlpatterns = [
    # views via ViewSet (samples)
    # for ModelViewSet classes router is used, see bellow

    # views via GenericViews (samples)
    path("generics/task/<int:task_id>", TaskDetailGenericViews.as_view(), name="get-task-by-id"),

    # views via ApiViews classes (samples)
    path("api_views/tasks/", TasksApiViews.as_view(), name="tasks-api-view"),

    # views via functions (samples)
    path("function/all_tasks", get_all_tasks, name="get-all-tasks"),
    path("function/create_task", create_new_task, name="create-new-task"),
]

# #################### FOR MODEL VIEW SET ONLY #########################
router = DefaultRouter()  # For ModelViewSet only
router.register(r"model_view_set/category", CategoryViewSet)  # regular expression is used r"category"
router.register(r"model_view_set/status", StatusViewSet)  # regular expression is used r"status"
urlpatterns += router.urls  # Unparse all CRUD methods and add to urlpatterns
# ######################################################################
