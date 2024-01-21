# #################### Via ModelViewSet Classes ########################
# CONTENT:
#

from rest_framework.viewsets import ModelViewSet  # Added

from apps.api.serializers import (StatusSerializer,  # Added
                                  CategorySerializer)

from apps.todo.models import (Status,  # Added
                              Category)


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
