from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_USERNAME,
    USERNAME_CHECK,
)
from users.validators import username_validator


class User(AbstractUser):
    """Класс для настройки модели юзера."""

    first_name = models.CharField(
        verbose_name='Фамилия Имя',
        max_length=MAX_LENGTH_USERNAME,
    )

    username = models.CharField(
        max_length=MAX_LENGTH_USERNAME,
        verbose_name='Логин',
        unique=True,
        db_index=True,
        validators=[RegexValidator(
            regex=USERNAME_CHECK,
            message='Имя пользователя содержит недопустимый символ'
        ),
            username_validator,
        ]
    )
    email = models.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        verbose_name='email',
        unique=True
    )

    avatar = models.ImageField(
        upload_to='user/',
        null=True,
        default=None,
        verbose_name='Фотография',
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Team(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название команды',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_teams',
        verbose_name='Владелец команды',
    )
    members = models.ManyToManyField(
        User,
        related_name='teams',
        blank=True,
        verbose_name='Участники команды',
    )

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.name
