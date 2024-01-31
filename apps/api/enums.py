from enumchoicefield import ChoiceEnum
from django.utils.translation import gettext_lazy
from rest_framework.fields import BooleanField

class YesNoChoiceEnum(ChoiceEnum):
    Yes = True
    No = False


class CustomTrueByDefaultBooleanField(BooleanField):
    default_empty_html = True
    initial = True
