# #################### Via GenericView Classes #########################
# CONTENT:
# Class TaskDetailGenericViews(RetrieveAPIView)


from rest_framework.request import Request  # Added
from rest_framework.response import Response  # Added
from rest_framework import status  # Added
from rest_framework.generics import (get_object_or_404,  # Added
                                     RetrieveAPIView,
                                     ListAPIView,
                                     ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from apps.api.messages import (SUBTASK_SUCCESS_CREATED_MESSAGE,
                               SUBTASK_SUCCESS_DELETED_MESSAGE)

from apps.todo.models import (Task,
                              SubTask)

from apps.api.serializers import (TaskModelSerializer,
                                  TaskWithSubtasksModelSerializer,
                                  SubTaskModelSerializer)


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
