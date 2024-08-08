from django.db import models
from django.contrib.auth.models import User


class Reporte(models.Model):
    TIPOS_REPORTE = [
        ('preventivo', 'Preventivo'),
        ('reparacion', 'Reparación'),
        ('correctivo', 'Correctivo'),
        ('inspeccion_norma', 'Inspección Norma'),
        ('otros', 'Otros')
    ]

    archivo = models.FileField(upload_to='reportes/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cliente = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_reporte = models.CharField(max_length=20, choices=TIPOS_REPORTE, blank=True, null=True)

    def __str__(self):
        return f"Reporte {self.id} - {self.cliente} - {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')} - {self.get_tipo_reporte_display()}"

    class Meta:
        permissions = [
            ("can_see_reports", "Can see reporte"),
            ("can_upload_reports", "Can upload reporte"),
        ]


class Empleado(models.Model):

    CARGO_OPCIONES = [
        ('tecnico', 'Técnico'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    puesto = models.CharField(max_length=50, choices=CARGO_OPCIONES)
    fecha_creacion = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.puesto}'

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['apellido', 'nombre']

        permissions = [
            ("can_see_empleados", "Can see empleados")
        ]
