from django.core.management.base import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = CustomUser.objects.create(email="user@user.com")
        user.nickname = "user"
        user.set_password("1234")
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Пользователь {user} успешно создан"))
        self.stdout.write(self.style.SUCCESS(f"Login: '{user}'\nEmail: {user.email}\nPassword: '1234'"))
