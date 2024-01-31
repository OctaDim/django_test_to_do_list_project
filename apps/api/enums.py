from enumchoicefield import ChoiceEnum
from django.utils.translation import gettext_lazy

class YesNoChoiceEnum(ChoiceEnum):
    Yes = True
    No = False
