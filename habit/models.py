"""Модель привычки"""

from django.db import models

from config import settings


class Habit(models.Model):
    """Модель привычки"""

    title = models.CharField(
        unique=True, max_length=50, verbose_name="Название привычки", help_text="Заниматься спортом/Правильно питаться"
    )
    place = models.CharField(max_length=250, verbose_name="Место", help_text="на работе/в спортзале/дома")
    action = models.CharField(max_length=50, verbose_name="Действие", help_text="пить воду/бегать")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits", verbose_name="Создатель привычки"
    )

    PERIODICITY_CHOICES = [
        (1, "Ежедневно"),
        (2, "Раз в 2 дня"),
        (3, "Раз в 3 дня"),
        (4, "Раз в 4 дня"),
        (5, "Раз в 5 дня"),
        (6, "Раз в 6 дня"),
        (7, "Еженедельно"),
    ]

    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки", help_text="Признак, что привычка является приятной"
    )

    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="main_habits",
        verbose_name="Связанная привычка",
        help_text="Приятная привычка, связанная с выполнением этой привычки",
        limit_choices_to={"is_pleasant": True},
    )

    periodicity = models.PositiveIntegerField(
        choices=PERIODICITY_CHOICES,
        default=1,
        verbose_name="Периодичность",
        help_text="Периодичность выполнения привычки в днях",
    )

    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Чем пользователь должен себя вознаградить после выполнения",
    )

    execution_time = models.PositiveIntegerField(
        verbose_name="Время на выполнение (в минутах)",
        help_text="Время, которое предположительно потратит пользователь на выполнение привычки",
    )

    is_public = models.BooleanField(
        default=False, verbose_name="Признак публичности", help_text="Публичная привычка видна всем пользователям"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    last_completed = models.DateTimeField(blank=True, null=True, verbose_name="Дата последнего выполнения")

    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        unique_together = [
            ("title", "place", "action", "user"),
        ]

    def __str__(self):
        habit_type = "Приятная" if self.is_pleasant else "Полезная"
        if self.reward:
            return f"{habit_type} привычка: {self.action}, награда: {self.reward}"
        if self.related_habit:
            return f"{habit_type} привычка: {self.action}, награда: {self.related_habit.action}"
        else:
            return f"{habit_type} привычка: {self.action},без награды"
