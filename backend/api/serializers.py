from django.contrib.auth import password_validation
from djoser.serializers import UserCreateSerializer, TokenCreateSerializer
from django.core.exceptions import ObjectDoesNotExist
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from tasks.models import Task, Team
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'avatar']


class CustomUserCreateSerializer(UserCreateSerializer):
    """Кастомный сериализатор для создания объекта класса User."""

    class Meta(UserCreateSerializer.Meta):
        """Кастомный сериализатор для входа в аккаунт."""

        model = User
        fields = [
            'id', 'first_name', 'username',
            'email', 'password',
        ]


class CustomTokenCreateSerializer(TokenCreateSerializer):
    """Сериализатор для получения токена."""

    password = serializers.CharField(
        required=False, style={'input_type': 'password'})

    class Meta():
        model = User
        fields = ['password']


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для аватара."""

    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ['avatar']

    def validate(self, data):
        """Проверка наличия аватара."""
        if data.get('avatar') is None:
            raise serializers.ValidationError('Данное поле обязательно.')
        return data


class PasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля."""

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class TaskSerializer(serializers.ModelSerializer):
    executor = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        required=False,
        allow_null=True
    )
    responsible = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at',
                  'updated_at', 'executor', 'responsible', 'team']
        read_only_fields = ['created_at', 'updated_at']


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'owner', 'members']

    def validate_name(self, value):
        """
        Ensure the team name is unique for the owner.
        """
        request_user = self.context['request'].user
        team_id = self.instance.id if self.instance else None
        if Team.objects.filter(name=value, owner=request_user).exclude(id=team_id).exists():
            raise serializers.ValidationError(
                'Имя команды с таким названием уже существует для этого пользователя.')
        return value

    def update(self, instance, validated_data):

        members = validated_data.pop('members', None)
        if members is not None:
            instance.members.set(members)
        return super().update(instance, validated_data)
