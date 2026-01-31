# Project5

## Команды для наполнения базы данных:
Для наполнения базы данных выполните последовательно следующие команды:
- Создайте суперпользователя командой "python manage.py create_superuser"
- Создайте пользователя командой "python manage.py createuser"

### Отложенные задачи

Запуск celery и worker (на Windows):
celery -A config worker -l INFO --pool=eventlet

### Тесты

Запуск:  coverage run --source='.' manage.py test
Отчет:  coverage html


### Документация
http://localhost:8000/swagger/ для Swagger UI 
http://localhost:8000/redoc/ для Redoc.