from django.contrib import admin

from tasks.models import Task, Team


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Класс настройки раздела тегов."""

    list_display = (
        'id',
        'title',
        'description',
        'status',
        'executor',
        'created_at',
        'updated_at',

    )
    list_display_links = ('id', 'title',)
    empty_value_display = 'значение отсутствует'
    search_fields = ('title',)


@admin.register(Team)
class TagAdmin(admin.ModelAdmin):
    """Класс настройки раздела тегов."""

    list_display = (
        'id',
        'name',
        'owner',
        'get_members',

    )
    list_display_links = ('id', 'name',)
    empty_value_display = 'значение отсутствует'
    search_fields = ('name',)

    def get_members(self, obj):
        return ", ".join([user.username for user in obj.members.all()])
    get_members.short_description = 'Участники команды'
