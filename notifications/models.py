from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField()

    def __str__(self):
        return self.name
