from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny

from habit.models import Habit
from habit.paginators import MyPaginator
from habit.permissions import IsOwner
from habit.serializers import HabitSerializer


class HabitCreateAPIView(CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitListAPIView(ListAPIView):
    """Для всех публичных привычек"""

    queryset = Habit.objects.filter(is_public=True, is_active=True).order_by("-created_at")
    serializer_class = HabitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "action", "periodicity", "place", "execution_time"]
    pagination_class = MyPaginator
    permission_classes = [AllowAny]


class HabitSelfListAPIView(ListAPIView):
    """Для всех публичных привычек"""

    serializer_class = HabitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "action", "periodicity", "place", "execution_time"]
    pagination_class = MyPaginator
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Habit.objects.filter(is_active=True, user=self.request.user).order_by("-created_at")


class HabitRetrieveAPIView(RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class HabitUpdateAPIView(UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    # permission_classes = [IsOwnerOrIsModerator]
    permission_classes = [IsOwner]


class HabitDestroyAPIView(DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]
