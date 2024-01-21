# #################### Via GenericView Classes #########################
# CONTENT:
# Class TaskDetailGenericViews(RetrieveAPIView)

from rest_framework.generics import (RetrieveAPIView,
                                     ListAPIView,
                                     get_object_or_404,

                                     )

from apps.api.serializers import (TaskSerializer,
                                  TaskWithSubtasksSerializer)
from apps.todo.models import Task


class GetTaskGenericViews(RetrieveAPIView):  # Parent class has the only 'get' method, so it will be inherited
    serializer_class = TaskSerializer

    def get_object(self):
        task_id = self.kwargs.get("task_id")
        task = get_object_or_404(Task, id=task_id)
        return task


class GetTaskWithSubtasksGenericViews(RetrieveAPIView):
    serializer_class = TaskWithSubtasksSerializer

    def get_object(self):
        task_id = self.kwargs.get("task_id")
        task = get_object_or_404(Task, id=task_id)
        return task


class GetAllTasksWithSubtasksGenericViews(ListAPIView):
    serializer_class = TaskWithSubtasksSerializer
    queryset = Task.objects.all()
