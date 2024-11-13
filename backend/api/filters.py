import django_filters

from users.models import Team


class TeamFilter(django_filters.FilterSet):
    
    members_username = django_filters.CharFilter(
        field_name='members__username', lookup_expr='icontains', label="Member Username")

    class Meta:
        model = Team
        fields = ['members_username']
