from django.urls import include, path
from rest_framework import routers

from api.views import TaskViewSet, TeamViewSet, UserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'task', TaskViewSet, basename='task')
router.register(r'team', TeamViewSet, basename='team')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]