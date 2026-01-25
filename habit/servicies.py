import requests
from django.contrib.auth import get_user_model
from django.utils import timezone

from config.settings import TELEGRAM_BOT_TOKEN
from habit.models import Habit


def get_today_habits(user_id):
    """Получаем список всех привычек на сегодня"""
    User = get_user_model()
    user = User.objects.get(id=user_id)
    habits = Habit.objects.filter(is_active=True, user=user)
    today = timezone.now()
    today_habits = []

    for habit in habits:
        if habit.last_completed:
            # Вычисляем разницу в днях
            difference = today - habit.last_completed
            days_difference = difference.days

            # Проверяем, прошло ли достаточно дней для следующего выполнения
            # days_difference >= habit.periodicity означает, что пора выполнять
            if days_difference >= habit.periodicity:
                today_habits.append(habit)
        else:
            # Если привычка никогда не выполнялась, добавляем ее в список на сегодня
            today_habits.append(habit)

    return today_habits


def complete_habit(habit_id):
    """Функция выполнения привычки"""
    habit = Habit.objects.get(id=habit_id)
    habit.last_completed = timezone.now()
    habit.save()


def tg_session(user, habits):
    """Создание сессию для отправки сообщений в телеграмм"""
    message = "Ваши привычки на сегодня:\n"
    for habit in habits:
        message += f"{habit}\n"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": user.telegram_id,
        "text": message,
    }
    response = requests.post(url, json=payload)
    return response.json()
