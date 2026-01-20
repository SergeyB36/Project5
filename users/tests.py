from io import StringIO
from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser
from users.serializers import CustomUserSerializer
from users.views import CustomUserCreateAPIView

User = get_user_model()


class CustomUserTestCase(APITestCase):
    """Тестирование CRUD операций для уроков"""

    def setUp(self):
        """Настройка тестовых данных. Создание user"""
        self.url = reverse('users:register')
        self.user = User.objects.create(nickname="testuser", email="testuser@test.com")
        self.user.set_password("1234")
        self.user.save()

    def test_create_user(self):
        """Тест создания пользователя user"""
        user = User.objects.get(nickname="testuser")

        self.assertEqual(user.nickname, 'testuser')
        self.assertEqual(user.email, 'testuser@test.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)

    def test_unique_nickname(self):
        """Тест уникальности nickname"""
        response = self.client.post(
            self.url,
            data={
                'nickname': 'testuser',
                'email': 'testuser@test.com',
                'password': '1234'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nickname', response.data)


    def test_unique_email(self):
        """Тест уникальности email"""
        response = self.client.post(
            self.url,
            data={
                'nickname': 'testuser1',
                'email': 'testuser@test.com',
                'password': '1234'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_invalid_data_nickname(self):
        """Тест невалидных данных при создании"""
        response = self.client.post(
            self.url,
            data={
                'nickname': '',
                'email': '',
                'password': '123'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nickname', response.data)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)

    def test_str_user(self):
        """Тест строкового представления"""
        user = User.objects.get(nickname="testuser")
        self.assertEqual(str(user), 'testuser')


class CustomUserCreateAPIViewTestCase(APITestCase):
    """Тесты для полного покрытия views.py"""

    def setUp(self):
        self.view = CustomUserCreateAPIView()
        self.url = reverse('users:register')
        self.valid_data = {
            'nickname': 'testuser',
            'email': 'testuser@test.com',
            'password': '1234'
        }

    def test_serializer_class_attribute(self):
        """Тест: serializer_class установлен корректно"""
        self.assertEqual(self.view.serializer_class, CustomUserSerializer)

    def test_queryset_attribute(self):
        """Тест: queryset установлен корректно"""
        self.assertEqual(str(self.view.queryset.query), str(CustomUser.objects.all().query))

    # def test_permission_classes_attribute(self):
    #     """Тест что permission_classes установлен как AllowAny"""
    #     from rest_framework.permissions import AllowAny
    #     self.assertEqual(self.view.permission_classes, [AllowAny])

    def test_perform_create_method_called(self):
        """Тест: perform_create вызывается при создании"""
        view = CustomUserCreateAPIView()

        serializer_data = {
            'nickname': 'testuser',
            'email': 'testuser@test.com',
            'password': '1234'
        }
        serializer = CustomUserSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())

        view.perform_create(serializer)

        user = CustomUser.objects.get(email='testuser@test.com')

        self.assertTrue(user.is_active)

        self.assertNotEqual(user.password, '1234')
        self.assertTrue(user.check_password('1234'))


class CustomUserManagementCommandsTestCase(APITestCase):
    def test_command_creates_superuser(self):
        """Тест: создаем кастомной командой superuser"""

        self.assertEqual(User.objects.count(), 0)

        out = StringIO()

        call_command('create_superuser', stdout=out)

        output = out.getvalue()
        self.assertIn('Пользователь admin с правами superuser успешно создан', output)
        self.assertIn("Login: 'admin'", output)
        self.assertIn("Email: admin@user.com", output)
        self.assertIn("Password: '1234'", output)

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.get(email='admin@user.com')
        self.assertEqual(user.nickname, 'admin')
        self.assertTrue(user.check_password('1234'))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_command_creates_user(self):
        """Тест: создаем кастомной командой user"""

        self.assertEqual(User.objects.count(), 0)

        out = StringIO()

        call_command('createuser', stdout=out)

        output = out.getvalue()
        self.assertIn('Пользователь user успешно создан', output)
        self.assertIn("Login: 'user'", output)
        self.assertIn("Email: user@user.com", output)
        self.assertIn("Password: '1234'", output)

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.get(email='user@user.com')
        self.assertEqual(user.nickname, 'user')
        self.assertTrue(user.check_password('1234'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
