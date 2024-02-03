from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    AuthUser, )

from rest_framework_simplejwt.tokens import Token
from apps.user.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user=user)

        token["email"] = user.email
        token["username"] = user.username
        token["user_first_name"] = user.first_name
        token["user_last_name"] = user.last_name
        token["user_full_name"] = user.get_full_name

        return token
