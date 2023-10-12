from django.contrib import admin
from .models import Venta


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('fecha_venta', 'total_venta', 'es_fiado', 'usuario')
