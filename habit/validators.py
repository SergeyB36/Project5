from rest_framework.exceptions import ValidationError


class ExecutionTimeValidator:
    """Валидатор время на выполнение привычки"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        validated_value = value.get(self.field)
        min_value = 2
        max_value = 120
        if validated_value:
            if min_value <= validated_value <= max_value:
                return
            else:
                raise ValidationError("Время должно быть не менее 1 минуты и не должно превышать 120 минут")


class RewardValidator:
    """Валидатор награды"""

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        # Получаем значения полей
        reward = attrs.get(self.field)
        related_habit = attrs.get("related_habit")
        is_pleasant = attrs.get("is_pleasant")

        # Если привычка приятная, не должно быть вознаграждения или связанной привычки
        if is_pleasant and (reward or related_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки")

        # Если указаны и вознаграждение, и связанная привычка - это ошибка
        if reward and related_habit:
            raise ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку. Выберите что-то одно."
            )


class RelatedHabitValidator:
    """Валидатор для связанной привычки"""

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        # Получаем значение поля
        related_habit = attrs.get(self.field)
        if related_habit:
            if not related_habit.is_pleasant:
                # Связанная привычка должна быть приятной
                raise ValidationError("Связанная привычка может быть только приятной")
