"""Сериализатор модели привычки"""

from rest_framework.serializers import ModelSerializer

from habit.models import Habit
from habit.validators import (
    ExecutionTimeValidator,
    RelatedHabitValidator,
    RewardValidator,
)


class HabitSerializer(ModelSerializer):

    class Meta:
        model = Habit
        fields = [
            "title",
            "place",
            "action",
            "periodicity",
            "reward",
            "related_habit",
            "execution_time",
            "last_completed",
            "created_at",
            "user",
            "is_pleasant",
        ]
        read_only_fields = ["last_completed", "created_at", "user", "created_at"]
        validators = [
            ExecutionTimeValidator(field="execution_time"),
            RewardValidator(field="reward"),
            RelatedHabitValidator(field="related_habit"),
        ]
