from django.db import models
from django.contrib.auth.models import User


class Venta(models.Model):
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)
    es_fiado = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Venta del {self.fecha_venta} - Total: {self.total_venta}"
