from rest_framework import serializers  # Added

from apps.api.error_messages import (CATEGORY_NAME_LEN_ERROR_MESSAGE,  # Added
                                     STATUS_NAME_LEN_ERROR_MESSAGE,
                                     PASSWORDS_DO_NOT_MATCH_ERROR,
                                     USERNAME_ALREADY_EXISTS,
                                     EMAIL_ALREADY_EXISTS)

from apps.todo.models import (Task,  # Added
                              SubTask,
                              Category,
                              Status, )

from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy

from rest_framework.validators import UniqueValidator



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
    subtasks = SubTaskPreviewModelSerializer(many=True,  # Defining related serializer of the related Model to show
                                             read_only=True)  # info from SubTask serializer, when Task info showing

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


class UserRegisterSerializer(serializers.ModelSerializer):  # VLD
    email = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        style={"placeholder": "enter email like [any]@[any].[any]"}, )

    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        style={"placeholder": "enter your login"}, )

    password = serializers.CharField(min_length=4, max_length=68,
                                     write_only=True,
                                     style={"input_type": "password",
                                            "placeholder": "enter password"}, )

    password2 = serializers.CharField(min_length=4, max_length=68,
                                      write_only=True,
                                      style={"input_type": "password",
                                             "placeholder": "repeat password"}, )

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            "username",  # DIM
            'password',
            'password2'
        ]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        if password and password2 and (password != password2):
            raise serializers.ValidationError(
                gettext_lazy(PASSWORDS_DO_NOT_MATCH_ERROR))

        # username_to_check_unique = attrs.get("username")  # Check, if not defined unique validator in field parameters
        # if User.objects.filter(username=username_to_check_unique).exists():
        #     raise serializers.ValidationError(
        #         gettext_lazy(USERNAME_ALREADY_EXISTS))
        #
        # email_to_check_unique = attrs.get("email")  # Check, if not defined unique validator in field parameters
        # if User.objects.filter(email=email_to_check_unique).exists():
        #     raise serializers.ValidationError(
        #         gettext_lazy(EMAIL_ALREADY_EXISTS))

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            username=validated_data.get("username"),
            password=validated_data.get("password")
        )

        return user


class UserListSerializer(serializers.ModelSerializer):  # VLD
    class Meta:
        model = User
        fields = '__all__'


class UserInfoSerializer(serializers.ModelSerializer):  # VLD
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'username',
            # 'phone',  # Not in standard User Model
            'date_joined'
        ]
