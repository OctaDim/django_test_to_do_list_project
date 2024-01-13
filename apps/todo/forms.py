from django.forms import (ModelForm, fields, ModelChoiceField)  # Added
from apps.todo.models import (User, Category, Status, Task)  # Added
from django.forms import widgets


class CreateTaskForm(ModelForm):
    title = fields.CharField(max_length=50)
    description = fields.CharField(max_length=1500, widget=fields.Textarea)
    creator = ModelChoiceField(queryset=User.objects.all())
    category = ModelChoiceField(queryset=Category.objects.all(), required=False)
    status = ModelChoiceField(queryset=Status.objects.all())

    start_date = fields.DateField(
        widget=widgets.DateInput(attrs={"type": "data"}))

    deadline_date = fields.DateField(
        widget=widgets.DateInput(attrs={"type": "data"}))

    class Meta:
        model = Task
        fields = "__all__"
