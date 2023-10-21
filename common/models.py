from django.db import models
from django.contrib.auth.models import User


class ColombiaDepartments(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ColombiaCities(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(
        'ColombiaDepartments', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class PendingMsgView(models.Model):
    text = models.TextField(blank=True)
    error_code = models.CharField(max_length=300, blank=True)
    creado_por = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    to = models.IntegerField(blank=True, null=True)
    fecha_creación = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cliente} - {self.text}'
