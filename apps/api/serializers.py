from rest_framework import serializers  # Added

from apps.todo.models import (Task,
                              SubTask,
                              Category,
                              Status, )


class AllTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id",
                  "title",
                  "description",
                  "creator",
                  "category",
                  "status",
                  "start_date",
                  "deadline_date",
                  "note", ]
        # fields = "__all_"  # if all fields/
