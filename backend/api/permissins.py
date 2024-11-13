from rest_framework import permissions


class IsUserorAdmin(permissions.BasePermission):
    """Класс доступа для обычного пользователя"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.id == request.user.id
                or request.user.is_superuser)
