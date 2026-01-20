from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from habit.models import CustomUser


class CustomUserSerializer(ModelSerializer):
    subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "nickname", "avatar", "email", "subscriptions"]
        read_only_fields = ["id",]

    def get_subscriptions(self, obj):
        return obj.user_subscription.filter(is_active=True)