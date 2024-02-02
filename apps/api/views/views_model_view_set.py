# #################### Via ModelViewSet Classes ########################
# CONTENT:
#
from rest_framework.viewsets import ModelViewSet  # Added

from apps.api.serializers import (StatusModelSerializer,  # Added
                                  CategoryModelSerializer)

from apps.todo.models import (Status,  # Added
                              Category)

from rest_framework.permissions import (IsAuthenticated,  # Added
                                        IsAdminUser,
                                        AllowAny)

class StatusViewSet(ModelViewSet):  # All CRUD methods are under the hood included
    queryset = Status.objects.all()
    serializer_class = StatusModelSerializer


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    # All CRUD methods are under the hood included
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
