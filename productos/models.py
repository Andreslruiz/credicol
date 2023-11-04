from django.db import models

from django.contrib.auth.models import User


class Producto(models.Model):

    UNIDAD_CHOICES = [
        ('kilo', 'KG'),
        ('libra', 'LB'),
        ('gramos', 'GRM'),
        ('galon', 'GL'),
        ('litro', 'LT'),
        ('cuarto litro', '1/4 LT'),
        ('ml', 'ML'),
        ('unidad', 'UND'),
        ('metros', 'MT'),
        ('centimetro', 'CM'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    precio = models.IntegerField(default=0)
    compania = models.ForeignKey(
        'companies.CompanyProfile', on_delete=models.CASCADE
    )
    activo = models.BooleanField(default=True)
    creado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    stock = models.IntegerField(blank=True, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
