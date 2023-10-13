from django.contrib import admin
from import_export.admin import ImportExportMixin, ExportActionModelAdmin

from .models import Transaccion
from .resources import TransaccionesResource


@admin.register(Transaccion)
class CompanyProfileAdmin(
    ImportExportMixin, ExportActionModelAdmin, admin.ModelAdmin
):
    resource_class = TransaccionesResource
    list_display = (
        'tipo_transaccion', 'fecha_transaccion',
        'total_transaccion', 'es_fiado', 'usuario'
    )
