from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Класс настройки раздела пользователи."""

    list_display = (
        'id',
        'first_name',
        'username',
        'email',
        'avatar',
    )
    list_display_links = ('id', 'first_name',)
    empty_value_display = 'значение отсутствует'
    search_fields = ('first_name', 'username', 'email',)
