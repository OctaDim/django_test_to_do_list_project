from django.db import models

from apps.todo.models_helpers import create_default_description


# Create your models here.

class Task(models.Model):
    # id = models.UUIDField  # NOTE: If hashed id is necessary, not int number
    # id = models.IntegerField(primary_key=True,    # NOTE: In Django is
    #                          auto_created = True, # auto-generating field
    #                          serialize = False,   # with the default
    #                          verbose_name = 'ID') # settings under the hood

    # email = models.EmailField  # Only Django sugar field. Under the hood - VARCHAR with validation
    # models.CommaSeparatedIntegerField  # Only Django sugar field. Under the hood - VARCHAR with validation
    # models.IPAddressField  # Only Django sugar field. Under the hood - VARCHAR with validation
    title = models.CharField(max_length=75,
                             default="DEFAULT TITLE")  # Hardcoded default value
    description = models.TextField(
        max_length=1500,
        verbose_name="Task details",  # For displaying in admin panel
        default=create_default_description)  # Func 'create_default_description' returns, when new record is creating
    start_date = models.DateField(help_text="Day, when the task should be started")
    deadline_date = models.DateField(help_text="Day, when the task should be finished")
    started_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
