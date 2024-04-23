import locale

from django.db import models


class ClienteProfile(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    apellido = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    credit_balance = models.FloatField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(
        'companies.CompanyProfile', on_delete=models.CASCADE,
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = 'Perfil de Clientes'
        verbose_name_plural = 'Perfiles de Clientes'
        permissions = [
            ('can_see_initial_view', 'Puede ver vista inicial'),
            ('can_see_clientes', 'Puede ver lista clientes'),
            ('can_create_cliente', 'Puede crear cliente'),
            ('can_ver_cliente', 'Puede ver detalle cliente'),
            ('can_edit_cliente', 'Puede editar cliente')
        ]

    @property
    def deuda(self):
        if self.credit_balance:
            # locale.setlocale(locale.LC_ALL, 'es_CO.utf8')
            # deuda = locale._format("%d", self.credit_balance, grouping=True)
            return self.credit_balance

        return '0'
