""" Сериализатор модель пользователя """
from rest_framework.serializers import ModelSerializer

from habit.models import CustomUser


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "nickname", "avatar", "email"]
        read_only_fields = ["id",]
