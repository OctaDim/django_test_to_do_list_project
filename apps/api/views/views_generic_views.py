# #################### Via GenericView Classes #########################
# CONTENT:
# Class TaskDetailGenericViews(RetrieveAPIView)

from rest_framework.generics import (RetrieveAPIView,
                                     get_object_or_404,
                                     )

from apps.api.serializers import AllTasksSerializer
from apps.todo.models import Task


class TaskDetailGenericViews(RetrieveAPIView):
    serializer_class = AllTasksSerializer

    def get_object(self):
        task_id = self.kwargs.get("task_id")
        task = get_object_or_404(Task, id=task_id)
        return task
