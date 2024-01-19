import django.utils.timezone
from django.contrib.auth.models import User
from django.db.models import Model
from django.db import models

from apps.todo.models_helpers import create_default_description  # Added


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    objects = models.Manager()  # Defining default objects manager

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Status(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    objects = models.Manager()  # Defining default objects manager

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class Task(models.Model):
    title = models.CharField(max_length=75,
                             default="DEFAULT TITLE")  # Hardcoded default value
    # (unique=True)
    # (unique_for_date= 'start_date')  # Field should be unique for this date
    # (unique_for_month= '')           # string linc to any date field
    # (unique_for_year= '')             # string linc to any date field
    # id = models.UUIDField  # NOTE: If hashed id is necessary, not int number
    # id = models.IntegerField(primary_key=True,    # NOTE: In Django is
    #                          auto_created = True, # auto-generating field
    #                          serialize = False,   # with the default
    #                          verbose_name = 'ID') # settings under the hood
    # email = models.EmailField  # Only Django sugar field. Under the hood - VARCHAR with validation
    # models.CommaSeparatedIntegerField  # Only Django sugar field. Under the hood - VARCHAR with validation
    # models.IPAddressField  # Only Django sugar field. Under the hood - VARCHAR with validation

    description = models.TextField(
        max_length=1500,
        null=True, blank=True,
        verbose_name="Task details",  # For displaying in admin panel
        default=create_default_description)  # Func 'create_default_description' returns, when new record is creating

    creator = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    # creator = models.ForeignKey(to_field="name", on_delete=models.CASCADE)  # key to another field
    # creator = models.ForeignKey(User, on_delete=models.DO_NOTHING) When deleting user, do nothing
    # creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # creator = models.ForeignKey(User, default="def on delete user", on_delete=models.SET_DEFAULT)
    # creator = models.ForeignKey(User, on_delete=models.SET(111))
    # creator = models.ForeignKey(User, on_delete=models.SET("def on delete user"))

    category = models.ForeignKey(Category,
                                 default=1,
                                 blank=True, null=True,
                                 on_delete=models.SET_NULL)

    status = models.ForeignKey(Status,
                               default=1,
                               null=True, blank=True,
                               on_delete=models.SET(1))

    start_date = models.DateField(
        # editable=True,
        # auto_now_add=True, # Make False, because FormModel cannot have non-editable field
        null=True, blank=True,
        help_text="Day, when the task should be started")

    deadline_date = models.DateField(
        # editable=True,
        # auto_now_add=True,
        null=True, blank=True,
        help_text="Day, when the task should be finished")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    deleted = models.BooleanField(
        default=False, editable=False)  # NOTE!!!: by default value is None, if not redefined

    note = models.CharField(max_length=250, null=True, blank=True)

    objects = models.Manager()  # Defining default objects manager

    def __str__(self):
        if len(str(self.title)) > 15:
            return f"{self.title[:15]}..."
        else:
            return self.title[:15]

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class SubTask(models.Model):
    title = models.CharField(max_length=75, default="DEFAULT SUBTASK")
    description = models.TextField(max_length=1500, null=True, blank=True)

    category = models.ForeignKey(Category, default=1,
                                 blank=True, null=True,
                                 on_delete=models.SET_NULL)

    task = models.ForeignKey(Task, default=1,
                             on_delete=models.CASCADE,
                             related_name="subtasks")

    creator = models.ForeignKey(User, default=1,
                                on_delete=models.CASCADE)

    status = models.ForeignKey(Status, default=1,
                               null=True, blank=True,
                               on_delete=models.CASCADE)
    # status = models.ForeignKey(Status, default=1, on_delete=models.SET(1))

    start_date = models.DateField(null=True, blank=True,
                                  # auto_now_add=True,
                                  help_text="Day, when the task should be started")

    deadline_date = models.DateField(null=True, blank=True,
                                     # auto_now_add=True,
                                     help_text="Day, when the task should be finished")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    note = models.CharField(max_length=250, null=True, blank=True)

    objects = models.Manager()  # Defining default objects manager

    def __str__(self):
        if len(str(self.title)) > 15:
            return f"{self.title[:15]}..."
        else:
            return self.title[:15]

    class Meta:
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"
