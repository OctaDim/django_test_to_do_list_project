from rest_framework import serializers
from apps.user.models import User

class AppsUserUserAllFieldsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AppsUserUserByIdModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id",
                  "email",
                  "username",
                  "first_name",
                  "last_name",
                  "phone",
                  "date_joined",
                  "last_login"
                  ]
