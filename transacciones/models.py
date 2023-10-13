from django.db import models
from django.contrib.auth.models import User


class Transaccion(models.Model):
    TIPO_CHOICES = (
        ('venta', 'Venta'),
        ('pago', 'Pago'),
    )

    observaciones = models.CharField(max_length=500, blank=True)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    total_transaccion = models.DecimalField(max_digits=10, decimal_places=2)
    es_fiado = models.BooleanField(default=False)
    tipo_transaccion = models.CharField(
        max_length=5, choices=TIPO_CHOICES, blank=True, null=True
    )

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    cliente = models.ForeignKey(
        'clientes.ClienteProfile', on_delete=models.CASCADE,
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.tipo_transaccion}: {self.total_transaccion}"
