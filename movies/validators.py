from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def validate_0_100_rating(value):
    if not 0 <= int(value) <= 100:
        raise ValidationError(
            gettext_lazy('Rating должен быть в диапозоне от 0 до 100. %(value)s не подходит'),
            params={'value': value}
        )
    # data = {'value': 4}, здесь data это params
    # '%(value)s привет' % data <=> '{value} привет'.format(**data)
