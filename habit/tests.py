from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
User = get_user_model()

class HabitTestCase(APITestCase):
    """Тестирование CRUD операций для уроков"""

    def setUp(self):
        """Настройка тестовых данных. Создание привычки №1"""
        # Пользователь 1
        self.user1 = User.objects.create(nickname="testuser1", email="testuser1@test.com")
        self.user1.set_password("1234")
        self.user1.save()

        # Пользователь 2
        self.user2 = User.objects.create(nickname="testuser2", email="testuser2@test.com")
        self.user2.set_password("1234")
        self.user2.save()

        # Привычки пользователя 1
        # Ежедневная
        self.habit = Habit.objects.create(title="Правильно питаться", place="дома и на работе", action="Пить воду", periodicity="DAILY", execution_time=30, user=self.user1)
        self.habit.save()
        # Еженедельная
        self.habit = Habit.objects.create(title="Вести спортивный образ жизни", place="в спортзале", action="подтягиваться на турнике 10 раз", periodicity="WEEKLY", execution_time=100, user=self.user1)
        self.habit.save()
        # Ежемесячная
        self.habit = Habit.objects.create(title="Зарабатывать деньги", place="на работе", action="получать зарплату", periodicity="MONTHLY", execution_time=10, user=self.user1)
        self.habit.save()
        # Привычки пользователя 2
        # Ежедневная
        self.habit = Habit.objects.create(title="Вести приятный образ жизни", place="в кабаке", action="Играть в видеоигры", periodicity="DAILY", execution_time=100, user=self.user2)
        self.habit.save()
        # Еженедельная
        self.habit = Habit.objects.create(title="Отдыхать", place="дома", action="пить пиво", periodicity="WEEKLY", execution_time=100, user=self.user2)
        self.habit.save()
        # Ежемесячная
        self.habit = Habit.objects.create(title="Пойти в магазин", place="на улице", action="тратить деньги", periodicity="MONTHLY", execution_time=100, user=self.user2)
        self.habit.save()

    def test_create_habit(self):
        """Тест получения данных из БД"""
        habit = Habit.objects.get(title="Правильно питаться")

        self.assertEqual(habit.periodicity, 'DAILY')
        self.assertEqual(habit.action, 'Пить воду')
        self.assertEqual(habit.place, 'дома и на работе')
        self.assertEqual(habit.execution_time, 30)
        self.assertTrue(habit.is_active)


    def test_list_habit(self):
        """Тест получения списка привычек и пагинации"""
        self.url = reverse('habit:habit-list')
        response_page1 = self.client.get(
            self.url
        )
        self.assertEqual(response_page1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_page1.data['results']), 5)
        response_page2 = self.client.get(response_page1.data['next'])
        self.assertEqual(response_page1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_page2.data['results']), 1)

    #
    #
    # def test_unique_email(self):
    #     """Тест уникальности email"""
    #     response = self.client.post(
    #         self.url,
    #         data={
    #             'nickname': 'testuser1',
    #             'email': 'testuser@test.com',
    #             'password': '1234'
    #         },
    #         format='json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('email', response.data)
    #
    # def test_invalid_data_nickname(self):
    #     """Тест невалидных данных при создании"""
    #     response = self.client.post(
    #         self.url,
    #         data={
    #             'nickname': '',
    #             'email': '',
    #             'password': '123'
    #         },
    #         format='json'
    #     )
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('nickname', response.data)
    #     self.assertIn('email', response.data)
    #     self.assertIn('password', response.data)
    #
    # def test_str_user(self):
    #     """Тест строкового представления"""
    #     user = User.objects.get(nickname="testuser")
    #     self.assertEqual(str(user), 'testuser')