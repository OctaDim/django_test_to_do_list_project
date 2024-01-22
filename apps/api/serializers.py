from rest_framework import serializers  # Added

from apps.api.error_messages import (CATEGORY_NAME_LEN_ERROR_MESSAGE,  # Added
                                     STATUS_NAME_LEN_ERROR_MESSAGE)

from django.contrib.auth.models import User
from apps.todo.models import (Task,  # Added
                              SubTask,
                              Category,
                              Status, )


class ExampleSerializer(serializers.Serializer):  # Low-level Serializer sample. Enables define field parameters

    title = serializers.CharField(max_length=50, required=True)  # Defining fields parameters

    def create(self, validated_data):  # Overriding methods. Sample: Low-level Serializer class inheritance
        pass

    class Meta:  # Sample: Low-level Serializer class inheritance
        model = Task
        fields = ["id", "title", "description"]


class StatusModelSerializer(serializers.ModelSerializer):  # ModelSerialize takes all fields parameters from the Model
    class Meta:
        model = Status
        fields = "__all__"

    def validate_name(self, value):  # def validate_<model_field_name> - for each field method name, value= field value
        if not 3 < len(value) < 30:
            raise serializers.ValidationError(STATUS_NAME_LEN_ERROR_MESSAGE)


class CategoryModelSerializer(serializers.ModelSerializer):  # ModelSerializer: all fields parameters from the Model

    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):  # def validate_<model_field_name> - for each field method name, value= field value
        if not 4 < len(value) < 25:
            raise serializers.ValidationError(CATEGORY_NAME_LEN_ERROR_MESSAGE)


class TaskModelSerializer(serializers.ModelSerializer):  # ModelSerializer takes all fields parameters from the Model

    # SlugRelatedField (see bellow) allow to edit fields and simultaneously
    # and show literal value from model __str__ method instead of id value
    category = serializers.SlugRelatedField(slug_field="name",
                                            queryset=Category.objects.all())

    creator = serializers.SlugRelatedField(slug_field="username",
                                           queryset=User.objects.all())

    status = serializers.SlugRelatedField(slug_field="name",
                                          queryset=Status.objects.all())

    # StringRelatedField (see bellow) show literal value from model __str__ method, instead of id value,
    # but makes fields read_only=True by default, so fields cannot be edited
    # creator = serializers.StringRelatedField()
    # category = serializers.StringRelatedField()
    # status = serializers.StringRelatedField()

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


class SubTaskModelSerializer(serializers.ModelSerializer):
    # SlugRelatedField (see bellow) allow to edit fields and simultaneously
    # and show literal value from model __str__ method instead of id value
    category = serializers.SlugRelatedField(slug_field="name",
                                            queryset=Category.objects.all(), )

    creator = serializers.SlugRelatedField(slug_field="username",
                                           queryset=User.objects.all())

    status = serializers.SlugRelatedField(slug_field="name",
                                          queryset=Status.objects.all())

    task = serializers.SlugRelatedField(slug_field="title",
                                        queryset=Task.objects.all())

    # StringRelatedField (see bellow) show literal value from model __str__ method, instead of id value,
    # but makes fields read_only=True by default, so fields cannot be edited
    # creator = serializers.StringRelatedField()
    # category = serializers.StringRelatedField()
    # status = serializers.StringRelatedField()
    # task = serializers.StringRelatedField()

    class Meta:
        model = SubTask
        fields = ["id",
                  "title",
                  "description",
                  "category",
                  "task",
                  "creator",
                  "status",
                  "start_date",
                  "deadline_date",
                  "note", ]


class SubTaskPreviewModelSerializer(serializers.ModelSerializer):  # ModelSerializer: all fields params from the Model

    # SlugRelatedField (see bellow) allow to edit fields and simultaneously
    # and show literal value from model __str__ method instead of id value
    category = serializers.SlugRelatedField(slug_field="name",
                                            queryset=Category.objects.all())

    creator = serializers.SlugRelatedField(slug_field="username",
                                           queryset=User.objects.all())

    status = serializers.SlugRelatedField(slug_field="name",
                                          queryset=Status.objects.all())

    # StringRelatedField (see bellow) show literal value from model __str__ method, instead of id value,
    # but makes fields read_only=True by default, so fields cannot be edited
    # creator = serializers.StringRelatedField()
    # category = serializers.StringRelatedField()
    # status = serializers.StringRelatedField()

    class Meta:
        model = SubTask
        fields = ["id",
                  "title",
                  "category",
                  "status",
                  "description",
                  "creator",
                  "task",
                  "note", ]


class TaskWithSubtasksModelSerializer(serializers.ModelSerializer):  # ModelSerializer all fields params from the Model

    # SlugRelatedField (see bellow) allow to edit fields and simultaneously
    # and show literal value from model __str__ method instead of id value
    category = serializers.SlugRelatedField(slug_field="name",
                                            queryset=Category.objects.all())

    creator = serializers.SlugRelatedField(slug_field="username",
                                           queryset=User.objects.all())

    status = serializers.SlugRelatedField(slug_field="name",
                                          queryset=Status.objects.all())

    # StringRelatedField (see bellow) show literal value from model __str__ method, instead of id value,
    # but makes fields read_only=True by default, so fields cannot be edited
    # creator = serializers.StringRelatedField()
    # category = serializers.StringRelatedField()
    # status = serializers.StringRelatedField()

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
