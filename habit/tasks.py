from celery import shared_task
from django.contrib.auth import get_user_model

from habit.servicies import get_today_habits, tg_session

User = get_user_model()


@shared_task
def tg_notification():
    """Функция оповещения пользователя"""
    telegram_users = User.objects.filter(is_active=True)

    for user in telegram_users:
        # Получаем привычки пользователя на сегодня
        habits = get_today_habits(user.id)

        if habits and user.telegram_id:
            # Формируем сводное сообщение
            tg_session(user, habits)
