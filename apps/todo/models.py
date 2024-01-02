from django.db import models


# Create your models here.

class Task(models.Model):
    # id = models.UUIDField  # NOTE: If hashed id is necessary, not int number
    # id = models.IntegerField(primary_key=True,  # NOTE: In Django is
    #                          unique=True,       # auto-generating field
    #                          null=False,        # with the default
    #                          auto_created=True) # settings under the hood

    # email = models.EmailField  # Only Django sugar field. Under the hood - VARCHAR with validation
    # models.CommaSeparatedIntegerField  # Only Django sugar field. Under the hood - VARCHAR with validation
    # models.IPAddressField  # Only Django sugar field. Under the hood - VARCHAR with validation
    title = models.CharField(max_length=75)
    description = models.TextField(max_length=1500)
    start_date = models.DateField()
    deadline_date = models.DateField()
    started_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
