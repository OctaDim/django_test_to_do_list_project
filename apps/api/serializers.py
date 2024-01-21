from rest_framework import serializers  # Added

from apps.api.error_messages import (CATEGORY_NAME_LEN_ERROR_MESSAGE,  # Added
                                     STATUS_NAME_LEN_ERROR_MESSAGE)

from apps.todo.models import (Task,  # Added
                              SubTask,
                              Category,
                              Status, )


class ExampleSerializer(serializers.Serializer):  # Low-level Serializer class inherittance sample. Enables define field parameters
    title = serializers.CharField(max_length=50, required=True)  # Defining fields parameters

    def create(self, validated_data):  # Overriding methods. Sample: Low-level Serializer class inherittance
        pass

    class Meta:  # Sample: Low-level Serializer class inherittance
        model = Task
        fields = ["id", "title", "description"]


class TaskSerializer(serializers.ModelSerializer):  # ModelSerializer takes all fields parameters from the Model
    creator = serializers.StringRelatedField()  # Shows literal value from model __str__ method, instead of id value
    category = serializers.StringRelatedField()  # Shows literal value from model __str__ method, instead of id value
    status = serializers.StringRelatedField()  # Shows literal value from model __str__ method, instead of id value

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


class SubTaskPreviewSerializer(serializers.ModelSerializer):  # ModelSerializer takes all fields parameters from the Model
    status = serializers.StringRelatedField()  # Shows literal value from model __str__ method, instead of id value
    category = serializers.StringRelatedField()  # Shows literal value from model __str__ method, instead of id value

    class Meta:
        model = SubTask
        fields = ["id",
                  "title",
                  "category",
                  "status",
                  "description",
                  "note", ]


class TaskWithSubtasksSerializer(serializers.ModelSerializer):  # ModelSerializer takes all fields parameters from the Model
    subtasks = SubTaskPreviewSerializer(many=True, read_only=True)  # Defining related serializer of the related Model

    creator = serializers.StringRelatedField()  # Shows literal value from model __str__ method, instead of id value
    category = serializers.StringRelatedField()  # Shows literal value from model __str__ method, instead of id value
    status = serializers.StringRelatedField()  # Shows literal value from model __str__ method, instead of id value

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


class StatusSerializer(serializers.ModelSerializer):  # ModelSerializer takes all fields parameters from the Model
    class Meta:
        model = Status
        fields = "__all__"

    def validate_name(self, value):  # def validate_<model_field_name> - for each field method name, value= field value
        if not 3 < len(value) < 30:
            raise serializers.ValidationError(STATUS_NAME_LEN_ERROR_MESSAGE)



class CategorySerializer(serializers.ModelSerializer):  # ModelSerializer takes all fields parameters from the Model
    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):  # def validate_<model_field_name> - for each field method name, value= field value
        if not 4 < len(value) < 25:
            raise serializers.ValidationError(CATEGORY_NAME_LEN_ERROR_MESSAGE)
