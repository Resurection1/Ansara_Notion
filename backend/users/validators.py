from django.core.exceptions import ValidationError

from users.constants import NAME_ME


def username_validator(value):
    if value == NAME_ME:
        raise ValidationError(f'Использовать имя "{NAME_ME}" запрещено')
