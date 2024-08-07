from django.db import models
from django.contrib.auth.models import User


class Reporte(models.Model):
    TIPOS_REPORTE = [
        ('preventivo', 'Preventivo'),
        ('reparacion', 'Reparación'),
        ('correctivo', 'Correctivo'),
        ('inspeccion_norma', 'Inspección Norma'),
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
