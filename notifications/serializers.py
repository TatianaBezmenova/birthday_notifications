import datetime

from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet


class CustomJSONEncoder(DjangoJSONEncoder):
    """Кастомный сериализатор для преобразования формата даты."""
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.strftime('%d.%m.%Y')  # Здесь Вы можете задать нужный формат даты
        return super().default(obj)


def custom_serialize(queryset: QuerySet) -> str:
    """Преобразует queryset в json используя кастомный сериализатор."""
    return serialize('json', queryset, cls=CustomJSONEncoder)
