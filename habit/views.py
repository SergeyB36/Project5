from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny

from habit.models import Habit
from habit.paginators import MyPaginator
from habit.serializers import HabitSerializer


class HabitCreateAPIView(CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]

    # permission_classes = [CanCreatePermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitListAPIView(ListAPIView):
    queryset = Habit.objects.all().order_by('-created_at')
    serializer_class = HabitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "action", "periodicity", "place", "execution_time"]
    pagination_class = MyPaginator
    permission_classes = [AllowAny]


class HabitRetrieveAPIView(RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]


class HabitUpdateAPIView(UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    # permission_classes = [IsOwnerOrIsModerator]
    permission_classes = [AllowAny]


class HabitDestroyAPIView(DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    # permission_classes = [IsOwner]
    permission_classes = [AllowAny]
