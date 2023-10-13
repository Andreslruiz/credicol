from django.contrib import admin
from .models import Transaccion


@admin.register(Transaccion)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'tipo_transaccion', 'fecha_transaccion',
        'total_transaccion', 'es_fiado', 'usuario'
    )
