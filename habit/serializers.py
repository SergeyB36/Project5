""" Сериализатор модели привычки """
from rest_framework.serializers import ModelSerializer

from habit.models import Habit


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = ["title", "place", "action", "periodicity", "reward", "execution_time", "last_completed", "created_at", "user"]
        read_only_fields = ["last_completed", "created_at", "user", "created_at"]
