from rest_framework import serializers  # Added

from apps.api.error_messages import (CATEGORY_NAME_LEN_ERROR_MESSAGE,  # Added
                                     STATUS_NAME_LEN_ERROR_MESSAGE,
                                     PASSWORDS_DO_NOT_MATCH_ERROR,
                                     USERNAME_ALREADY_EXISTS,
                                     EMAIL_ALREADY_EXISTS,
                                     PASSWORDS_ALL_REQUIRED_MESSAGE
                                     )

from apps.todo.models import (Task,  # Added
                              SubTask,
                              Category,
                              Status)

# ####################################################
# from django.contrib.auth.models import User  # Added
from apps.user.models import User
# ####################################################

from django.utils.translation import gettext_lazy
from rest_framework.validators import UniqueValidator

from enumchoicefield import EnumChoiceField, ChoiceEnum

from apps.api.enums import YesNoChoiceEnum
from apps.api.enums import CustomTrueByDefaultBooleanField


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
                  "note",
                  ]
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
                  "note",
                  ]


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
                  "note",
                  ]


class TaskWithSubtasksModelSerializer(serializers.ModelSerializer):  # ModelSerializer all fields params from the Model
    # Defining related serializer of the related Model to show
    # info from SubTask serializer, when Task info showing
    subtasks = SubTaskPreviewModelSerializer(many=True,
                                             read_only=True)

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
                  "subtasks",
                  ]


class RegistrationUserSerializer(serializers.ModelSerializer):  # VLD
    email = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        style={"placeholder": "enter email like <any>@<any>.<any>"}, )

    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        style={"placeholder": "enter your login"}, )

    password = serializers.CharField(
        min_length=4, max_length=68,
        write_only=True,
        style={"input_type": "password",
               "placeholder": "enter password"}, )

    password2 = serializers.CharField(
        min_length=4, max_length=68,
        write_only=True,
        style={"input_type": "password",
               "placeholder": "repeat password"}, )

    class Meta:
        model = User
        fields = ["email",
                  "username",  # DM
                  "first_name",
                  "last_name",
                  "phone",
                  "password",
                  "password2",
                  ]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        ERROR_MESSAGES = []
        if not password or not password2:
            ERROR_MESSAGES.append(
                gettext_lazy(PASSWORDS_ALL_REQUIRED_MESSAGE))
            # raise serializers.ValidationError(
            #     gettext_lazy(PASSWORDS_ALL_REQUIRED_MESSAGE))

        if password != password2:
            ERROR_MESSAGES.append(
                gettext_lazy(PASSWORDS_DO_NOT_MATCH_ERROR))
            # raise serializers.ValidationError(
            #     gettext_lazy(PASSWORDS_DO_NOT_MATCH_ERROR))

        # # # Optionally fields can be checked without field parameters in this way
        # username_to_check_unique = attrs.get("username")  # Check, if not defined unique validator in field parameters
        # if User.objects.filter(username=username_to_check_unique).exists():
        #     ERROR_MESSAGES.append(gettext_lazy(USERNAME_ALREADY_EXISTS))
        #     # raise serializers.ValidationError(
        #     #     gettext_lazy(USERNAME_ALREADY_EXISTS))
        #
        # email_to_check_unique = attrs.get("email")  # Check, if not defined unique validator in field parameters
        # if User.objects.filter(email=email_to_check_unique).exists():
        #     ERROR_MESSAGES.append(gettext_lazy(EMAIL_ALREADY_EXISTS))
        #     # raise serializers.ValidationError(
        #     #     gettext_lazy(EMAIL_ALREADY_EXISTS))

        if ERROR_MESSAGES:
            raise serializers.ValidationError(ERROR_MESSAGES)

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data.get("email"),
                                    username=validated_data.get("username"),
                                    first_name=validated_data.get("first_name"),
                                    last_name=validated_data.get("last_name"),
                                    phone=validated_data.get("phone"),
                                    password=validated_data.get("password"),
                                    )
        return user


class RegistrationAdminStaffUserSerializer(serializers.ModelSerializer):  # VLD
    email = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        style={"placeholder": "enter email like <any>@<any>.<any>"}, )

    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        style={"placeholder": "enter your login"}, )

    password = serializers.CharField(
        min_length=4, max_length=68,
        write_only=True,
        style={"input_type": "password",
               "placeholder": "enter password"}, )

    password2 = serializers.CharField(
        min_length=4, max_length=68,
        write_only=True,
        style={"input_type": "password",
               "placeholder": "repeat password"}, )

    is_staff = CustomTrueByDefaultBooleanField()
    # is_staff = serializers.BooleanField()
    # is_staff = EnumChoiceField(enum_class=YesNoChoiceEnum,
    #                        default=YesNoChoiceEnum.No,
    #                        verbose_name="Staff group",
    #                        default=True,
    #                        )

    is_superuser = CustomTrueByDefaultBooleanField()
    # is_superuser = serializers.BooleanField()
    # is_superuser = EnumChoiceField(enum_class=YesNoChoiceEnum,
    #                                # default=YesNoChoiceEnum.Yes,
    #                                verbose_name="SuperUser",
    #                                #default=True,
    #                                )

    is_verified = CustomTrueByDefaultBooleanField()
    # is_verified = serializers.BooleanField()
    # is_verified = EnumChoiceField(enum_class=YesNoChoiceEnum,
    #                                # default=YesNoChoiceEnum.No,
    #                               verbose_name="Verified",
    #                               # default=True,
    #                               )

    class Meta:
        model = User
        fields = ["email",
                  "username",  # DM
                  "first_name",
                  "last_name",
                  "phone",
                  "password",
                  "password2",
                  "is_staff",
                  "is_superuser",
                  "is_verified"
                  ]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        ERROR_MESSAGES = []

        if not password or not password2:
            ERROR_MESSAGES.append(
                gettext_lazy(PASSWORDS_ALL_REQUIRED_MESSAGE))
            # raise serializers.ValidationError(
            #     gettext_lazy(PASSWORDS_ALL_REQUIRED_MESSAGE))

        if password != password2:
            ERROR_MESSAGES.append(
                gettext_lazy(PASSWORDS_DO_NOT_MATCH_ERROR))
            # raise serializers.ValidationError(
            #     gettext_lazy(PASSWORDS_DO_NOT_MATCH_ERROR))

        # username_to_check_unique = attrs.get("username")  # Check, if not defined unique validator in field parameters
        # if User.objects.filter(username=username_to_check_unique).exists():
        #     ERROR_MESSAGES.append(gettext_lazy(USERNAME_ALREADY_EXISTS))
        #     # raise serializers.ValidationError(
        #     #     gettext_lazy(USERNAME_ALREADY_EXISTS))

        # email_to_check_unique = attrs.get("email")  # Check, if not defined unique validator in field parameters
        # if User.objects.filter(email=email_to_check_unique).exists():
        #     ERROR_MESSAGES.append(gettext_lazy(EMAIL_ALREADY_EXISTS))
        #     # raise serializers.ValidationError(
        #     #     gettext_lazy(EMAIL_ALREADY_EXISTS))

        if ERROR_MESSAGES:
            raise serializers.ValidationError(ERROR_MESSAGES)

        return attrs

    def create(self, validated_data):
        user = User.objects.create_superuser(
                        email=validated_data.get("email"),
                        username=validated_data.get("username"),
                        first_name=validated_data.get("first_name"),
                        last_name=validated_data.get("last_name"),
                        phone=validated_data.get("phone"),
                        password=validated_data.get("password"),
                        is_staff=validated_data.get("is_staff"),
                        is_superuser=validated_data.get("is_superuser"),
                        is_verified=validated_data.get("is_verified"),
                        )
        return user


class ListUsersSerializer(serializers.ModelSerializer):  # VLD
    class Meta:
        model = User
        fields = "__all__"


class UserIByIdSerializer(serializers.ModelSerializer):  # VLD
    class Meta:
        model = User
        fields = ["id",
                  "email",
                  "username"
                  "first_name",
                  "last_name",
                  "phone",
                  "date_joined",
                  ]
