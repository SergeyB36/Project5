from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import CustomUser


# class CustomUserSerializer(ModelSerializer):
#     subscriptions = serializers.SerializerMethodField()
#
#     class Meta:
#         model = CustomUser
#         fields = ("id", "email", "avatar", "phone_number", "country", "subscriptions")
#
#     def get_subscriptions(self, obj):
#         return obj.user_subscription.filter(is_active=True)