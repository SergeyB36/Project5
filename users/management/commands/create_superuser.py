from django.core.management.base import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = CustomUser.objects.create(email="admin@user.com")
        user.set_password("1234")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Пользователь {user} с правами superuser успешно создан"))
        self.stdout.write(self.style.SUCCESS(f"Login: '{user}'\nPassword: '1234'"))
