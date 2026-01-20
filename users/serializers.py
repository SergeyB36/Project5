""" Сериализатор модель пользователя """
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from habit.models import CustomUser


class CustomUserSerializer(ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=4,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = ["id", "nickname", "avatar", "email", "password"]
        read_only_fields = ["id",]
