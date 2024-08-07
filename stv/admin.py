from django.contrib import admin
from .models import Reporte


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'ciudad', 'fecha_creacion', 'tecnico')
