from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from habit.servicies import get_today_habits, complete_habit

User = get_user_model()


class HabitTestCase(APITestCase):
    """Тестирование CRUD операций для уроков"""

    def setUp(self):
        """Настройка тестовых данных"""
        # Пользователь 1
        self.user1 = User.objects.create(nickname="testuser1", email="testuser1@test.com")
        self.user1.set_password("1234")
        self.user1.save()

        # Пользователь 2
        self.user2 = User.objects.create(nickname="testuser2", email="testuser2@test.com")
        self.user2.set_password("1234")
        self.user2.save()

        # Привычки пользователя 1

        self.habit = Habit.objects.create(
            title="Правильно питаться",
            place="дома и на работе",
            action="Пить воду",
            periodicity=1,
            execution_time=30,
            user=self.user1,
            is_public=True,
        )
        self.habit.save()

        self.habit = Habit.objects.create(
            title="Вести спортивный образ жизни",
            place="в спортзале",
            action="подтягиваться на турнике 10 раз",
            periodicity=7,
            execution_time=100,
            user=self.user1,
        )
        self.habit.save()

        self.habit = Habit.objects.create(
            title="Зарабатывать деньги",
            place="на работе",
            action="получать зарплату",
            periodicity=1,
            execution_time=10,
            user=self.user1,
        )
        self.habit.save()

        self.habit = Habit.objects.create(
            title="Вести приятный образ жизни",
            place="в кабаке",
            action="Играть в видеоигры",
            periodicity=1,
            execution_time=100,
            user=self.user1,
        )
        self.habit.save()

        self.habit = Habit.objects.create(
            title="Отдыхать",
            place="дома",
            action="пить пиво",
            periodicity=7,
            execution_time=100,
            user=self.user1,
            is_pleasant=True,
        )
        self.pk = self.habit.id
        self.habit.save()

        self.habit = Habit.objects.create(
            title="Пойти в магазин",
            place="на улице",
            action="тратить деньги",
            periodicity=1,
            execution_time=100,
            user=self.user1,
        )
        self.habit.save()

    def test_get_habit(self):
        """Тест получения данных из БД"""
        habit = Habit.objects.get(title="Правильно питаться")

        self.assertEqual(habit.periodicity, 1)
        self.assertEqual(habit.action, "Пить воду")
        self.assertEqual(habit.place, "дома и на работе")
        self.assertEqual(habit.execution_time, 30)
        self.assertTrue(habit.is_active)

    def test_list_self_habit(self):
        """Тест получения списка своих привычек и пагинации"""
        self.url = reverse("habit:habit-list-self")
        user = User.objects.get(nickname="testuser1")
        self.client.force_authenticate(user=user)
        response_page1 = self.client.get(self.url)
        self.assertEqual(response_page1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_page1.data["results"]), 5)
        response_page2 = self.client.get(response_page1.data["next"])
        self.assertEqual(response_page1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_page2.data["results"]), 1)

    def test_list_public_habit(self):
        """Тест получения списка публичных привычек"""
        self.url = reverse("habit:habit-list-public")
        user = User.objects.get(nickname="testuser2")
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_habit(self):
        """Тест создания привычки"""
        user = User.objects.get(nickname="testuser1")
        self.client.force_authenticate(user=user)
        self.url = reverse("habit:habit-create")
        response = self.client.post(
            self.url,
            {
                "title": "Тест название",
                "place": "Тест место",
                "reward": "Тест награда",
                "action": "Тест действие",
                "periodicity": 7,
                "execution_time": 99,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["user"], user.id)
        self.assertEqual(response.data["place"], "Тест место")
        self.assertEqual(response.data["action"], "Тест действие")
        self.assertEqual(response.data["periodicity"], 7)
        self.assertEqual(response.data["title"], "Тест название")
        self.assertEqual(response.data["execution_time"], 99)

    def test_validators_habit(self):
        """Тест валидации данных привычки"""
        user = User.objects.get(nickname="testuser1")
        self.client.force_authenticate(user=user)
        self.user1.set_password("1234")
        self.url = reverse("habit:habit-create")
        # Тест валидации поля execution_time (2-120)
        response = self.client.post(
            self.url,
            {
                "title": "Тест название",
                "place": "Тест место",
                "action": "Тест действие",
                "periodicity": 7,
                "execution_time": 130,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            self.url,
            {
                "title": "Тест название",
                "place": "Тест место",
                "action": "Тест действие",
                "periodicity": 7,
                "execution_time": 1,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            self.url,
            {
                "title": "Тест название",
                "place": "Тест место",
                "is_pleasant": True,
                "reward": "Пожрать",
                "action": "Тест действие",
                "periodicity": 7,
                "execution_time": 6,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        is_pleasant_related_habit_id = Habit.objects.get(title="Отдыхать").id
        not_is_pleasant_related_habit_id = Habit.objects.get(title="Пойти в магазин").id

        response = self.client.post(
            self.url,
            {
                "title": "Тест название",
                "place": "Тест место",
                "reward": "Пожрать",
                "related_habit": not_is_pleasant_related_habit_id,
                "action": "Тест действие",
                "periodicity": 7,
                "execution_time": 6,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            self.url,
            {
                "title": "Тест название",
                "place": "Тест место",
                "related_habit": not_is_pleasant_related_habit_id,
                "action": "Тест действие",
                "periodicity": 7,
                "execution_time": 6,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            self.url,
            {
                "title": "Тест название",
                "place": "Тест место",
                "action": "Тест действие",
                "related_habit": is_pleasant_related_habit_id,
                "periodicity": 7,
                "execution_time": 120,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_habit(self):
        """Тест получения привычки"""
        habit = Habit.objects.get(title="Отдыхать")
        periodicity = habit.periodicity
        action = habit.action
        place = habit.place
        user = User.objects.get(nickname="testuser2")
        self.client.force_authenticate(user=user)
        self.url = reverse("habit:habit-retrieve", kwargs={"pk": habit.pk})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user = User.objects.get(nickname="testuser1")
        self.client.force_authenticate(user=user)
        self.url = reverse("habit:habit-retrieve", kwargs={"pk": habit.pk})
        response = self.client.get(self.url)
        self.assertEqual(response.data["periodicity"], int(periodicity))
        self.assertEqual(response.data["action"], action)
        self.assertEqual(response.data["place"], place)
        self.assertEqual(response.data["periodicity"], 7)

    def test_update_habit(self):
        """Тест обновления привычки"""
        habit = Habit.objects.get(title="Отдыхать")
        place = habit.place
        user = User.objects.get(nickname="testuser1")
        self.client.force_authenticate(user=user)
        new_plaсe = "в горах"

        self.url = reverse("habit:habit-retrieve", kwargs={"pk": habit.pk})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["place"], place)
        self.url = reverse("habit:habit-update", kwargs={"pk": habit.pk})
        response = self.client.patch(self.url, {"place": new_plaсe})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.url = reverse("habit:habit-retrieve", kwargs={"pk": habit.pk})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["place"], new_plaсe)

    def test_delete_habit(self):
        """Тест удаления привычки"""
        habit = Habit.objects.get(title="Отдыхать")
        habit2 = Habit.objects.get(title="Пойти в магазин")
        habit3 = Habit.objects.get(title="Вести приятный образ жизни")
        # list all
        user = User.objects.get(nickname="testuser1")
        self.client.force_authenticate(user=user)
        self.url = reverse("habit:habit-list-self")
        response_page1 = self.client.get(self.url)
        self.assertEqual(response_page1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_page1.data["results"]), 5)
        response_page2 = self.client.get(response_page1.data["next"])
        self.assertEqual(response_page1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_page2.data["results"]), 1)
        self.url = reverse("habit:habit-delete", kwargs={"pk": habit.id})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.url = reverse("habit:habit-delete", kwargs={"pk": habit2.id})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.url = reverse("habit:habit-list-self")
        response = self.client.get(self.url)
        self.assertEqual(response_page1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)

        user = User.objects.get(nickname="testuser2")
        self.client.force_authenticate(user=user)
        self.url = reverse("habit:habit-delete", kwargs={"pk": habit3.id})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SevicesTestCase(APITestCase):
    """Тестирование сервисных функций"""

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

    def test_get_habit_for_send(self):
        today = timezone.now()
        user = User.objects.get(nickname="testuser1")
        user1 = User.objects.get(nickname="testuser2")
        self.client.force_authenticate(user=user)
        self.url = reverse("habit:habit-create")
        response = self.client.post(
            self.url,
            {
                "title": "Тест название",
                "place": "Тест место",
                "reward": "Тест награда",
                "action": "Тест действие",
                "periodicity": 2,
                "execution_time": 99,
                "is_active": True,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            self.url,
            {
                "title": "Тест название вып",
                "place": "Тест место вып",
                "reward": "Тест награда вып",
                "action": "Тест действие вып",
                "periodicity": 1,
                "execution_time": 99,
                "is_active": True,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        today_habits1 = get_today_habits(user.id)
        self.assertEqual(len(today_habits1), 2)
        user1 = User.objects.get(nickname="testuser2")
        self.client.force_authenticate(user=user1)
        today_habits2 = get_today_habits(user1.id)
        self.assertEqual(len(today_habits2), 0)

    def test_get_not_complete_habit_for_send(self):
        user = User.objects.get(nickname="testuser1")
        self.client.force_authenticate(user=user)
        self.url = reverse("habit:habit-create")
        response = self.client.post(
            self.url,
            {
                "title": "Тест название",
                "place": "Тест место",
                "reward": "Тест награда",
                "action": "Тест действие",
                "periodicity": 2,
                "execution_time": 99,
                "is_active": True,
            },
        )
        habit1 = Habit.objects.get(title="Тест название")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            self.url,
            {
                "title": "Тест название 1",
                "place": "Тест место 1",
                "reward": "Тест награда 1",
                "action": "Тест действие 1",
                "periodicity": 1,
                "execution_time": 99,
                "is_active": True,
            },
        )
        # habit2 = Habit.objacts.get(title="Тест название1")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        today_habits = get_today_habits(user.id)
        self.assertEqual(len(today_habits), 2)
        complete_habit(habit1.id)
        today_habits1 = get_today_habits(user.id)
        self.assertEqual(len(today_habits1), 1)
        self.assertEqual(today_habits1[0].title, "Тест название 1")
