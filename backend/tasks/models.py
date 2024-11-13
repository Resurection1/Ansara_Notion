from django.contrib.auth import get_user_model
from django.db import models

from users.constants import MAX_LENGTH_USERNAME
from users.models import Team

User = get_user_model()


class Task(models.Model):
    STATUS_CHOICES = [
        ('created', 'Задача создана'),
        ('assigned', 'Назначен исполнитель'),
        ('completed', 'Задача выполнена'),
        ('verified', 'Задача проверена'),
    ]

    title = models.CharField(
        max_length=255,
        verbose_name='Название',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='Статус',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )
    executor = models.CharField(
        verbose_name='Исполнитель',
        max_length=MAX_LENGTH_USERNAME
    )
    responsible = models.ForeignKey(
        User,
        related_name='responsible_tasks',
        on_delete=models.CASCADE,
        verbose_name='Проверяющий',
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
        verbose_name='Команда',
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'Задача называется {self.title}'
