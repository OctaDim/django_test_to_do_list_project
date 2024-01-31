# #################### Via GenericView Classes #########################
# CONTENT:
# Class TaskDetailGenericViews(RetrieveAPIView)
# class TaskByIdGenericRetrieve(RetrieveAPIView)
# class TaskByIdWithSubtasksGenericRetrieve(RetrieveAPIView)
# class AllTasksWithSubtasksGenericList(ListAPIView)
# class AllSubtasksGenericListCreate(ListCreateAPIView)
# class SubtaskByIdGenericRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView)
# class TasksFilteredGenericListCreate(ListCreateAPIView)
# class RegisterUserGenericCreate(CreateAPIView)  # VLD
# class ListUsersGenericList(ListAPIView)  # VLD
# class UserByIdGenericRetrieveUpdDestroy(RetrieveUpdateDestroyAPIView)  # VLD


from rest_framework.request import Request  # Added
from rest_framework.response import Response  # Added
from rest_framework import status  # Added
from rest_framework.generics import (get_object_or_404,  # Added
                                     RetrieveAPIView,
                                     ListAPIView,
                                     ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     CreateAPIView)

from apps.api.messages import (SUBTASK_SUCCESS_CREATED_MESSAGE,
                               SUBTASK_SUCCESS_DELETED_MESSAGE)

from apps.todo.models import (Task,
                              SubTask)

from apps.api.serializers import (TaskModelSerializer,
                                  TaskWithSubtasksModelSerializer,
                                  SubTaskModelSerializer)

from rest_framework.permissions import (IsAuthenticated,  # VLD
                                        IsAdminUser,  # VLD
                                        AllowAny,  # VLD
                                        IsAuthenticatedOrReadOnly,
                                        DjangoModelPermissionsOrAnonReadOnly,  # ???
                                        DjangoModelPermissions,
                                        DjangoObjectPermissions,
                                        BasePermission,
                                        BasePermissionMetaclass)

from apps.api.serializers import (RegistrationUserSerializer,  # VLD
                                  RegistrationAdminStaffUserSerializer,
                                  ListUsersSerializer,  # VLD
                                  UserIByIdSerializer)  # VLD

# ####################################################
# from django.contrib.auth.models import User  # Added
from apps.user.models import User
# ####################################################


class TaskByIdGenericRetrieve(RetrieveAPIView):  # Parent class has the only 'get' method, so it will be inherited
    serializer_class = TaskModelSerializer

    def get_object(self):
        task_id = self.kwargs.get("task_id")
        task = get_object_or_404(Task, id=task_id)
        return task


class TaskByIdWithSubtasksGenericRetrieve(RetrieveAPIView):
    serializer_class = TaskWithSubtasksModelSerializer

    def get_object(self):
        task_id = self.kwargs.get("task_id")
        task = get_object_or_404(Task, id=task_id)
        return task


class AllTasksWithSubtasksGenericList(ListAPIView):
    serializer_class = TaskWithSubtasksModelSerializer
    queryset = Task.objects.all()


class AllSubtasksGenericListCreate(ListCreateAPIView):
    serializer_class = SubTaskModelSerializer

    def create_subtask(self, data):  # Custom function, not from Generic, as sample
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get_queryset(self):  # Overrode method instead of standard Generic method
        subtasks = SubTask.objects.filter(creator=self.request.user.id)
        return subtasks

    def get(self, request: Request, *args, **kwargs):
        """
            1) Get data from the Data Base via Model
            2) Check, if data exists
            3) Parse data via serializer (python objects -> JSON)
            4) Send response to the front
            """
        subtasks = self.get_queryset()

        if subtasks:
            serializer = self.serializer_class(instance=subtasks, many=True)
            return Response(status=status.HTTP_200_OK,
                            data=serializer.data)

        return Response(status=status.HTTP_204_NO_CONTENT,
                        data=[])

    def post(self, request: Request, *args, **kwargs):
        # Option 1: returns response with status code
        # serializer = self.serializer_class(data=request.data)
        #
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(status=status.HTTP_201_CREATED,
        #                     data=serializer.data)
        #
        # return Response(status=status.HTTP_400_BAD_REQUEST,
        #                 data=serializer.errors)

        # Option 2: sample, does not return response with error status code, option 1 is better (see bellow)
        new_subtask = self.create_subtask(data=request.data)

        return Response(status=status.HTTP_201_CREATED,
                        data=new_subtask)  # not serializer.data or serializer: funct already returned serializer.data


class SubtaskByIdGenericRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = SubTaskModelSerializer  # Minimum to work, if not defining and overriding included CRUD methods

    def get_object(self):  # Minimum to work if not defining and overriding included CRUD methods at all
        subtask_id = self.kwargs.get("subtask_id")
        subtask = get_object_or_404(SubTask, id=subtask_id)
        return subtask

    def update_subtask_info(self, instance=None):
        serializer = self.serializer_class(instance=instance,
                                           data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get(self, request: Request, *args, **kwargs):  # GenericMixin works without it, define, if overriding needed
        subtask = self.get_object()  # Get object defined in separate method, because it repeats in every CRUD method
        serializer = self.serializer_class(instance=subtask)
        return Response(status=status.HTTP_200_OK,
                        data=serializer.data)

    def put(self, request: Request, *args, **kwargs):  # GenericMixin works without it, define, if overriding needed
        subtask = self.get_object()
        updated_serialized_data = self.update_subtask_info(instance=subtask)
        return Response(status=status.HTTP_201_CREATED,
                        data={"data": updated_serialized_data,
                              "message": SUBTASK_SUCCESS_CREATED_MESSAGE})

    def delete(self, request: Request, *args, **kwargs):  # GenericMixin works without it, define, if overriding needed
        subtask = self.get_object()
        subtask.delete()
        return Response(status=status.HTTP_200_OK,
                        data=SUBTASK_SUCCESS_DELETED_MESSAGE)


class TasksFilteredGenericListCreate(ListCreateAPIView):
    serializer_class = TaskWithSubtasksModelSerializer

    # serializer_class = TaskModelSerializer

    def get_queryset(self):
        # 1) Get all tasks
        # 2) Get status abd category for each task
        # 3) Get list of the all subtasks for the current task

        queryset = (Task.objects
                    .select_related("category", "status")  # JOINing related one-many, one-one, minimize requests to DB
                    .prefetch_related("subtasks")  # JOINing many-many, , minimize requests number to DB
                    )

        # 4) Filtration by fields: status, category, [date_from, date_to], deadline_date
        #    note: values for the filtration will be passed via query_params
        #    sample: 127.0.0.1:8000/api/tasks/?status=NEW&category=WORK

        status_name = self.request.GET.get("status_name")
        category_name = self.request.GET.get("category_name")
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")
        deadline_date = self.request.GET.get("deadline_date")

        if status_name:
            queryset = queryset.filter(status__name=status_name)  # status__name refers to related model via field name

        if category_name:
            queryset = queryset.filter(category__name=category_name)  # category__name refer to related model via f.name

        if date_from and date_to:
            queryset = queryset.filter(start_date__range=[date_from,
                                                          date_to])

        if deadline_date:
            queryset = queryset.filter(deadline_date=deadline_date)

        return queryset

    def get(self, request: Request, *args, **kwargs):
        filtered_data = self.get_queryset()

        if filtered_data.exists():
            serializer = self.serializer_class(instance=filtered_data, many=True)
            return Response(status=status.HTTP_200_OK,
                            data=serializer.data)

        return Response(status=status.HTTP_204_NO_CONTENT,
                        data=[])

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK,
                        data=serializer.data)


# ########################## USER VIEWS ################################

class RegisterUserGenericCreate(CreateAPIView):
    permission_classes = [AllowAny, IsAuthenticated, IsAdminUser]  # JWT token doesn't understand
    serializer_class = RegistrationUserSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,
                            data=serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors)


class RegisterAdminStaffUserGenericCreate(CreateAPIView):
    permission_classes = [IsAdminUser]  # JWT token doesn't understand
    serializer_class = RegistrationAdminStaffUserSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,
                            data=serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors)


class ListUsersGenericList(ListAPIView):
    permission_classes = [IsAdminUser]  # JWT token doesn't understand
    serializer_class = ListUsersSerializer

    def get_queryset(self):
        users = User.objects.all()  # All users
        # users = User.objects.exclude(id=self.request.user.id)  # Except current user

        return users

    def get(self, request: Request, *args, **kwargs):
        users = self.get_queryset()

        if not users:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data=[])

        serializer = self.serializer_class(users, many=True)
        return Response(status=status.HTTP_200_OK,
                        data=serializer.data)


class UserByIdGenericRetrieveUpdDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]  # JWT token doesn't understand
    serializer_class = UserIByIdSerializer

    def get_object(self):
        user_id = self.kwargs.get("user_id")

        user_obj = get_object_or_404(User, id=user_id)

        return user_obj


    def get(self, request: Request, *args, **kwargs):
        user = self.get_object()

        serializer = self.serializer_class(user)

        return Response(status=status.HTTP_200_OK,
                        data=serializer.data)

    def put(self, request: Request, *args, **kwargs):
        user = self.get_object()

        serializer = self.serializer_class(user, data=request.data,
                                           partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data=serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors)

    def delete(self, request: Request, *args, **kwargs):
        user = self.get_object()

        user.delete()

        return Response(status=status.HTTP_200_OK,
                        data=[])
