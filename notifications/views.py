import datetime

from django.shortcuts import render

from notifications.consts import DAYS_COUNT, NO_BIRTHDAY_MESSAGE
from notifications.models import Employee


def index(request):
    """Страница уведомлений"""
    employees = get_birthday_data()

    return render(
        request, 'notifications/index.html', {'employees': employees, 'no_birthday_message': NO_BIRTHDAY_MESSAGE}
    )


def get_birthday_data():
    """Возвращает данные о днях рождения сотрудников."""
    on_date = datetime.date.today()
    query = Employee.objects.all()
    result = []

    for employee in query.iterator():
        birthday = employee.birthday
        birth_month_day = datetime.date(month=birthday.month, day=birthday.day, year=birthday.year)
        system_month_day = datetime.date(month=on_date.month, day=on_date.day, year=birthday.year)
        if 0 <= (system_month_day - birth_month_day).days <= DAYS_COUNT:
            result.append(employee)

    return result
