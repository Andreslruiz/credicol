from datetime import datetime, date
from datetime import timedelta

from django.db import models
from transacciones.models import Transaccion


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
            deuda = self.credit_balance
            deuda_formateada = "{:,.0f}".format(int(deuda))
            return "{}".format(deuda_formateada)

        return '0'

    @property
    def dias_mora(self):
        fecha_actual = date.today()
        deuda = self.deuda
        transacciones = Transaccion.objects.filter(cliente=self)
        deuda_clean = ''.join(c for c in deuda if c.isdigit())

        if int(deuda_clean) > 0 and transacciones:
            tr = Transaccion.objects.filter(cliente=self).order_by('-fecha_transaccion').first()
            ultimo_pago = tr.fecha_transaccion

            if isinstance(ultimo_pago, datetime):
                ultimo_pago = ultimo_pago.date()

            diferencia = fecha_actual - ultimo_pago

            dias_pasados = diferencia.days

        else:
            dias_pasados = 0

        if dias_pasados > 0:
            return dias_pasados

        return ''


class MembresiaEmpresas(models.Model):
    empresa = models.ForeignKey(
        'companies.CompanyProfile', on_delete=models.CASCADE,
        blank=True, null=True
    )

    registrada_el = models.DateTimeField(null=True, blank=True)
    valor_pagado = models.PositiveIntegerField(null=True, blank=True)
    dias_pagados = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.registrada_el and self.dias_pagados:
            self.empresa.fin_fecha_membresia = (
                self.registrada_el + timedelta(days=self.dias_pagados)
            )
            self.empresa.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.empresa} {self.empresa.fin_fecha_membresia}"
