""" Сериализатор модели привычки """
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from habit.models import Habit


class HabitSerializer(ModelSerializer):
    periodicity = SerializerMethodField()
    class Meta:
        model = Habit
        fields = ["title", "place", "email", "action", "periodicity", "reward", "execution_time", "last_completed", "created_at" ]
        read_only_fields = ["last_completed", "created_at"]
