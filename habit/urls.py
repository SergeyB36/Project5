from django.conf.urls.static import static
from django.urls import path
from rest_framework.permissions import AllowAny

from config import settings
from habit.views import HabitListAPIView, HabitCreateAPIView, HabitRetrieveAPIView, HabitDestroyAPIView, \
    HabitUpdateAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name


urlpatterns = [
    path("",HabitListAPIView.as_view(), name="habit-list"),
    path("create/", HabitCreateAPIView.as_view(), name="habit-create"),
    path("<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit-retrieve"),
    path("<int:pk>/delete/", HabitDestroyAPIView.as_view(), name="habit-delete"),
    path("<int:pk>/update/", HabitUpdateAPIView.as_view(), name="habit-update")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
