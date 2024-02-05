from django.urls import path  # Added
from rest_framework.routers import DefaultRouter  # Added, for ModelViewSet

from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

# views via functions (samples)
from apps.api.views.views_functions import (get_all_tasks,
                                            create_new_task, )
# views via ApiViews Classes (samples)
from apps.api.views.views_api_views import TasksApiViews

# views via GenericViews Classes (samples)
from apps.api.views.views_generic_views import (
                                TaskByIdGenericRetrieve,
                                TaskByIdWithSubtasksGenericRetrieve,
                                AllTasksWithSubtasksGenericList,
                                AllSubtasksGenericListCreate,
                                SubtaskByIdGenericRetrieveUpdateDelete,
                                TasksFilteredGenericListCreate,
                                RegisterUserGenericCreate,
                                RegisterAdminStaffUserGenericCreate,
                                ListUsersGenericList,
                                UserByIdGenericRetrieveUpdDestroy)

# views via ModelViewSet Classes (samples)
from apps.api.views.views_model_view_set import (StatusViewSet,
                                                 CategoryViewSet)

from apps.jwt_custom.views import CustomTokenObtainPairView

from apps.api.views.views_generic_views import (
    AppsUserListUsersExceptCurrentGenericList,
    AppsUserUserByIdGenericRetrieveUpdDestroy)



app_name = "api"

urlpatterns = [
    # views via ViewSet (samples):
    # --> for ModelViewSet classes DefaultRouter is used (see section bellow)

    # views via GenericViews (samples):
    path("generics/task/<int:task_id>/", TaskByIdGenericRetrieve.as_view(), name="get-task-by-id"),
    path("generics/task_with_subtasks/<int:task_id>/", TaskByIdWithSubtasksGenericRetrieve.as_view(), name="get-task-by-id-with-subtasks"),
    path("generics/all_tasks/", AllTasksWithSubtasksGenericList.as_view(), name="get-all-tasks"),
    path("generics/subtasks/", AllSubtasksGenericListCreate.as_view(), name="get-all-subtasks"),
    path("generics/subtask/<int:subtask_id>/", SubtaskByIdGenericRetrieveUpdateDelete.as_view(), name="get-subtask-by-id"),
    path("generics/filtered_tasks/", TasksFilteredGenericListCreate.as_view(), name="get-filtered-tasks"),

    # for users: views via GenericViews (samples):
    path("generics/auth/register_user/", RegisterUserGenericCreate.as_view(), name="register-new-user"),
    path("generics/auth/register_superuser/", RegisterAdminStaffUserGenericCreate.as_view(), name="register-new-superuser"),
    path("generics/auth/all_users-v1/", ListUsersGenericList.as_view(), name="get-all-users-v1"),
    path("generics/auth/user_by_id-v1/<int:user_id>/", UserByIdGenericRetrieveUpdDestroy.as_view(), name="get-user-by-id-v1"),

    path("generics/user/all_users-v2/", AppsUserListUsersExceptCurrentGenericList.as_view(), name="get-all-users-v2"),
    path("generics/user/user_by_id-v2/<int:user_id>/", AppsUserUserByIdGenericRetrieveUpdDestroy.as_view(), name="get-user-by-id-v2"),

    # for login and obtain, refresh Token: views via rest framework simple JWT:
    path("simple_jwt/auth/login_and_obtain_token/", TokenObtainPairView.as_view(), name="login-and-obtain-token"),
    path("simple_jwt/auth/login_and_obtain_custom_token/", CustomTokenObtainPairView.as_view(), name="login-and-obtain-custom-token"),
    path("simple_jwt/auth/refresh_token/", TokenRefreshView.as_view(), name="refresh-token"),

    # views via ApiViews classes (samples):
    path("api_views/tasks/", TasksApiViews.as_view(), name="tasks-api-view"),

    # views via functions (samples):
    path("function/all_tasks/", get_all_tasks, name="get-all-tasks"),
    path("function/create_task/", create_new_task, name="create-new-task"),
]

# #################### FOR MODEL VIEW SET ONLY: ########################
router = DefaultRouter()  # For ModelViewSet only
router.register(r"model_view_set/category", CategoryViewSet)  # regular expression is used r"category". WITHOT '/' at the end of url!!!
router.register(r"model_view_set/status", StatusViewSet)  # regular expression is used r"status". WITHOT '/' at the end of url!!!
urlpatterns += router.urls  # Unparse all CRUD methods and add to urlpatterns
# ######################################################################
