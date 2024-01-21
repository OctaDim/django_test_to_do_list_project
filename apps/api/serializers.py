from rest_framework import serializers  # Added

from apps.api.error_messages import (CATEGORY_NAME_LEN_ERROR_MESSAGE,  # Added
                                     STATUS_NAME_LEN_ERROR_MESSAGE)

from apps.todo.models import (Task,  # Added
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


class SubTaskPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ["id",
                  "title",
                  "category",
                  "status", ]


class TaskInfoSerializer(serializers.ModelSerializer):
    subtasks = SubTaskPreviewSerializer(many=True, read_only=True)

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
                  "note",
                  "subtasks", ]


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"

    def validate_name(self, value):  # def validate_<model_field_name> - for each field method name, value= field value
        if not 3 < len(value) < 30:
            raise serializers.ValidationError(STATUS_NAME_LEN_ERROR_MESSAGE)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):  # def validate_<model_field_name> - for each field method name, value= field value
        if not 4 < len(value) < 25:
            raise serializers.ValidationError(CATEGORY_NAME_LEN_ERROR_MESSAGE)
