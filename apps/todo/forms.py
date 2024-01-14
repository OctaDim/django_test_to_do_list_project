from django.forms import (ModelForm, fields, ModelChoiceField)  # Added
from apps.todo.models import (User, Category, Status, Task)  # Added
from django.forms import widgets


class CreateTaskForm(ModelForm):
    # See bellow how to define model and fields fast, without defining parameters
    title = fields.CharField(max_length=75)
    description = fields.CharField(max_length=1500, widget=fields.Textarea)
    creator = ModelChoiceField(queryset=User.objects.all())
    category = ModelChoiceField(queryset=Category.objects.all(), required=False)
    status = ModelChoiceField(queryset=Status.objects.all())

    start_date = fields.DateField(
        widget=widgets.DateInput(attrs={"type": "data"}))

    deadline_date = fields.DateField(
        widget=widgets.DateInput(attrs={"type": "data"}))

    note = fields.CharField(max_length=250)

    class Meta:
        model = Task
        fields = "__all__"


class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ("title", "description", "category", "status",
                  "start_date", "deadline_date", "note")  # Possible to choose necessary fields
        # fields = "__all__"  # All fields can be defined in this way
