from django.db import models


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

    WS = 'WS'
    MSG = 'MSG'

    TYPE_OPTIONS = [
        (WS, 'Whatsapp'),
        (MSG, 'MSG'),
    ]

    url = models.JSONField(max_length=500, blank=True)
    headers = models.JSONField(max_length=500, blank=True)
    data = models.JSONField(max_length=500, blank=True)
    type = models.CharField(choices=TYPE_OPTIONS, max_length=10)
    error_code = models.CharField(max_length=200, blank=True)
    fecha_creación = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.url} - {self.type}'
