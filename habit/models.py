""" Модель привычки """
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from config import settings


class Habit(models.Model):
    """Модель привычки"""
    title = models.CharField(
        unique=True,
        max_length=50,
        verbose_name="Название привычки",
        help_text="Заниматься спортом/Правильно питаться"
    )
    place = models.CharField(max_length=250, verbose_name="Место", help_text="на работе/в спортзале/дома")
    action = models.CharField(max_length=50, verbose_name="Действие", help_text="пить воду/бегать")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Создатель привычки'
    )
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

    PERIODICITY_CHOICES = [
        (DAILY, 'Ежедневно'),
        (WEEKLY, 'Еженедельно'),
        (MONTHLY, 'Ежемесячно'),
    ]

    DAYS_OF_WEEK = [
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресенье'),
    ]

    day_of_week = models.IntegerField(
        choices=DAYS_OF_WEEK,
        blank=True,
        null=True,
        verbose_name='День недели',
        help_text='День недели для выполнения (если привычка не ежедневная)'
    )

    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки',
        help_text='Признак, что привычка является приятной'
    )

    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='main_habits',
        verbose_name='Связанная привычка',
        help_text='Приятная привычка, связанная с выполнением этой привычки',
        limit_choices_to={'is_pleasant': True}
    )

    periodicity = models.CharField(
        max_length=10,
        choices=PERIODICITY_CHOICES,
        default=DAILY,
        verbose_name='Периодичность',
        help_text='Периодичность выполнения привычки'
    )

    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Вознаграждение',
        help_text='Чем пользователь должен себя вознаградить после выполнения'
    )

    execution_time = models.PositiveIntegerField(
        verbose_name='Время на выполнение (в минутах)',
        help_text='Время, которое предположительно потратит пользователь на выполнение привычки'
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности',
        help_text='Публичная привычка видна всем пользователям'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    last_completed = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата последнего выполнения'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )

    # def clean(self):
    #     """Валидация: только одно поле может быть заполнено"""
    #     from django.core.exceptions import ValidationError
    #
    #     if self.reward and self.related_habit:
    #         raise ValidationError(
    #             'Можно указать либо текстовое вознаграждение, либо связанную привычку, но не оба поля одновременно.'
    #         )
    #     if not self.reward and not self.related_habit:
    #         pass

    # def get_reward_display(self):
    #     """Метод для получения отображаемого значения награды"""
    #     if self.related_habit:
    #         return f"Привычка: {self.related_habit.title}"
    #     elif self.reward:
    #         return self.reward
    #     return "Нет вознаграждения"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        unique_together = [
            ("title", "place", "action", "user"),
        ]

    def __str__(self):
        habit_type = "Приятная" if self.is_pleasant else "Полезная"
        return f"{habit_type} привычка: {self.action}"
