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
        'get_responsible',
        'get_team',
        'created_at',
        'updated_at',

    )
    list_display_links = ('id', 'title',)
    empty_value_display = 'значение отсутствует'
    search_fields = ('title',)

    def get_responsible(self, obj):
        return ", ".join([user.username for user in obj.responsible.all()])
    get_responsible.short_description = 'Ответственные'

    def get_team(self, obj):
        if obj.team is not None:
            return ", ".join([user.username for user in obj.team.members.all()])
    get_team.short_description = 'Команда'


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
