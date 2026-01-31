from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        # Разрешаем доступ только аутентифицированным пользователям
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь владельцем объекта
        return obj.user == request.user
