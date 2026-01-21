from http.client import responses

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
        self.pk = self.habit.id
        self.habit.save()
        # Ежемесячная
        self.habit = Habit.objects.create(title="Пойти в магазин", place="на улице", action="тратить деньги", periodicity="MONTHLY", execution_time=100, user=self.user2)
        self.habit.save()

    def test_get_habit(self):
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

    def test_create_habit(self):
        """Тест создания привычки"""
        user = User.objects.get(nickname="testuser1")
        self.client.force_authenticate(user=user)
        self.user1.set_password("1234")
        self.url = reverse('habit:habit-create')
        response = self.client.post(
            self.url, {
                'title': "Тест название",
                'place': "Тест место",
                'action': "Тест действие",
                'periodicity': "weekly",
                'execution_time': 99
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['user'], user.id)
        self.assertEqual(response.data['place'], "Тест место")
        self.assertEqual(response.data['action'], "Тест действие")
        self.assertEqual(response.data['periodicity'], "weekly")
        self.assertEqual(response.data['title'], "Тест название")
        self.assertEqual(response.data['execution_time'], 99)

    def test_retrieve_habit(self):
        """Тест получения привычки"""
        habit = Habit.objects.get(title="Отдыхать")
        periodicity = habit.periodicity
        action = habit.action
        place = habit.place

        self.url = reverse('habit:habit-retrieve', kwargs={'pk': habit.pk})
        response = self.client.get(
            self.url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['periodicity'], periodicity)
        self.assertEqual(response.data['action'], action)
        self.assertEqual(response.data['place'], place)
        self.assertEqual(response.data['periodicity'], "WEEKLY")

    def test_update_habit(self):
        """Тест обновления привычки"""
        habit = Habit.objects.get(title="Отдыхать")
        place = habit.place
        new_plaсe = "в горах"

        self.url = reverse('habit:habit-retrieve', kwargs={'pk': habit.pk})
        response = self.client.get(
            self.url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], place)
        self.url = reverse('habit:habit-update', kwargs={'pk': habit.pk})
        response = self.client.patch(
            self.url, {'place': new_plaсe}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.url = reverse('habit:habit-retrieve', kwargs={'pk': habit.pk})
        response = self.client.get(
            self.url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], new_plaсe)

    def test_delete_habit(self):
        """Тест удаления привычки"""
        habit = Habit.objects.get(title='Отдыхать')
        habit2 = Habit.objects.get(title='Пойти в магазин')
        # list all
        self.url = reverse('habit:habit-list')
        response_page1 = self.client.get(
            self.url
        )
        self.assertEqual(response_page1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_page1.data['results']), 5)
        response_page2 = self.client.get(response_page1.data['next'])
        self.assertEqual(response_page1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_page2.data['results']), 1)
        self.url = reverse('habit:habit-delete', kwargs={'pk': habit.id})
        response = self.client.delete(
            self.url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.url = reverse('habit:habit-delete', kwargs={'pk': habit2.id})
        response = self.client.delete(
            self.url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.url = reverse('habit:habit-list')
        response = self.client.get(
            self.url
        )
        self.assertEqual(response_page1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)
