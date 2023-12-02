from django.shortcuts import render

from notifications.models import Employee


def index(request):
    employees = Employee.objects.all()
    return render(request, 'notifications/index.html', {'employees': employees})
