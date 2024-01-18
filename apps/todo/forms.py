from django.forms import ModelForm, fields, ModelChoiceField  # Added
from django.forms import widgets  # Added
from apps.todo.models import (User,
                              Category,
                              Status,
                              Task,
                              SubTask,
                              )  # Added


class CreateTaskForm(ModelForm):
    # See bellow how to define model and fields fast with fields parameters by default as defined in Model
    title = fields.CharField(max_length=75)
    description = fields.CharField(max_length=1500,
                                   widget=fields.Textarea,
                                   required=False, )
    creator = ModelChoiceField(queryset=User.objects.all(), )
    category = ModelChoiceField(queryset=Category.objects.all(),
                                required=False, )
    status = ModelChoiceField(queryset=Status.objects.all(),
                              required=False, )

    start_date = fields.DateField(
        widget=widgets.DateInput(attrs={"type": "data"}), required=False, )

    deadline_date = fields.DateField(
        widget=widgets.DateInput(attrs={"type": "data"}), required=False, )

    note = fields.CharField(max_length=250, required=False, )

    class Meta:
        model = Task
        fields = "__all__"  # fields = "__all__" All fields were defined in this way


class TaskUpdateForm(ModelForm):
    # define fields in easy way, but all formatting will be defined in templates in this way

    class Meta:
        model = Task
        fields = ("title", "description", "category", "status",
                  "start_date", "deadline_date", "note", )  # Possible to choose necessary fields
        # fields = "__all__"  # All fields can be defined in this way


class SubTaskUpdateForm(ModelForm):
    # define fields in easy way, but all formatting will be defined in templates in this way

    class Meta:
        model = SubTask
        fields = ("title", "description", "category", "status",
                  "start_date", "deadline_date", "note", )  # Possible to choose necessary fields
        # fields = "__all__"  # All fields can be defined in this way


class CreateSubTaskForm(ModelForm):
    class Meta:
        model = SubTask
        fields = ("title", "description", "category", "status",
                  "task", "creator", "note",
                  "start_date", "deadline_date", )
        # fields = "__all__"  # All fields can be defined in this way
