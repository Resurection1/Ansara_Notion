from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from api.constants import INCORRECT_PASSWORD
from api.filters import TeamFilter
from api.pagination import CastomPagePagination
from api.permissins import IsUserorAdmin
from api.serializers import (
    AvatarSerializer,
    CustomUserCreateSerializer,
    PasswordSerializer,
    TaskSerializer,
    TeamSerializer,
    UserSerializer,
)
from tasks.models import Task, Team
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User."""

    queryset = User.objects.order_by('id')
    permission_classes = (IsUserorAdmin, )
    pagination_class = CastomPagePagination
    filter_backends = (filters.SearchFilter, )
    filterset_fields = ('id',)
    search_fields = ('id', )
    lookup_field = 'id'
    http_method_names = (
        'patch', 'post', 'delete', 'put',
    )

    def get_serializer_class(self):
        """Условие для выбора сериализатора."""
        if self.action == 'create':
            return CustomUserCreateSerializer
        return UserSerializer

    @action(
        methods=('post',),
        detail=False,
        url_path='set_password',
        permission_classes=(permissions.IsAuthenticated, )
    )
    def set_password(self, request):
        """Смена пароля."""
        user = request.user
        serializer = PasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(
            serializer.validated_data['current_password']
        ):
            return Response(
                {'current_password': INCORRECT_PASSWORD},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('get', 'patch'),
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated, )
    )
    def get_patch_me(self, request):
        """Получение или изменения страницы me."""
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=('put', 'delete'),
        detail=False,
        url_path='me/avatar',
        permission_classes=(permissions.IsAuthenticated, )
    )
    def put_avatar(self, request):
        """Изменение аватара."""
        user = get_object_or_404(User, username=request.user.username)
        serializer = AvatarSerializer(user, data=request.data, partial=True)

        if request.method == 'PUT':
            serializer = AvatarSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {'avatar': user.avatar.url},
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        elif request.method == 'DELETE':
            user.avatar.delete()
            user.avatar = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = (
        'patch', 'post', 'delete', 'put',
    )

    def get_queryset(self):
        user = self.request.user

        return Task.objects.filter(
            Q(responsible=user) |
            Q(executor=user) |
            Q(team__members=user)
        ).distinct()

    def perform_create(self, serializer):
        user = self.request.user
        team = serializer.validated_data.get('team', None)

        if team and team.owner != user and not team.members.filter(
            id=user.id
        ).exists():
            raise PermissionDenied(
                'Только члены команды могут создавать задачи для этой команды.')
        serializer.save()


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TeamFilter

    def get_queryset(self):
        user = self.request.user
        return Team.objects.filter(
            owner=user
        ) | Team.objects.filter(members=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        team = self.get_object()

        if team.owner != request.user:
            raise PermissionDenied(
                'Только владелец может удалить эту команду.')
        return super().destroy(request, *args, **kwargs)
