from django.db import models
from django.contrib.auth.models import User


class Gasto(models.Model):

    observaciones = models.TextField(blank=True)
    fecha_gasto = models.DateTimeField(auto_now_add=True)
    total_gasto = models.DecimalField(max_digits=10, decimal_places=2)
    creada_por = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    company = models.ForeignKey(
        'companies.CompanyProfile', on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"{self.company}: {self.total_gasto}"

    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        permissions = [
            ('can_add_gasto', 'Puede añadir gasto'),
            ('can_edit_gasto', 'Puede editar gasto'),
        ]
