# #################### Via GenericView Classes #########################
# CONTENT:
# Class TaskDetailGenericViews(RetrieveAPIView)


from rest_framework.request import Request  # Added
from rest_framework.response import Response  # Added
from rest_framework import status  # Added
from rest_framework.generics import (RetrieveAPIView,  # Added
                                     ListAPIView,
                                     ListCreateAPIView,
                                     get_object_or_404)

from apps.api.serializers import (TaskModelSerializer,
                                  TaskWithSubtasksModelSerializer,
                                  SubTaskModelSerializer)
from apps.todo.models import (Task,
                              SubTask)


class TaskByIdGenericViewsRetrieve(RetrieveAPIView):  # Parent class has the only 'get' method, so it will be inherited
    serializer_class = TaskModelSerializer

    def get_object(self):
        task_id = self.kwargs.get("task_id")
        task = get_object_or_404(Task, id=task_id)
        return task


class TaskByIdWithSubtasksGenericViewsRetrieve(RetrieveAPIView):
    serializer_class = TaskWithSubtasksModelSerializer

    def get_object(self):
        task_id = self.kwargs.get("task_id")
        task = get_object_or_404(Task, id=task_id)
        return task


class AllTasksWithSubtasksGenericViewsList(ListAPIView):
    serializer_class = TaskWithSubtasksModelSerializer
    queryset = Task.objects.all()


class AllSubtasksGenericViewsListCreate(ListCreateAPIView):
    serializer_class = SubTaskModelSerializer

    def create_subtask(self, data):  # Custom function, not from Generic
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get_queryset(self):
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
        # new_subtask = self.create_subtask(data=request.data)
        # return Response(status=status.HTTP_201_CREATED,
        #                 data=new_subtask)  # not serializer, because functions returns result serializer.data already

        # Option 2: returns response with status code
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,
                            data=serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors)
