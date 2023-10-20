from django.contrib import admin
from import_export.admin import ImportExportMixin, ExportActionModelAdmin

from .models import Producto
from .resources import ProductoResource

@admin.register(Producto)
class ProductoAdmin(
    ImportExportMixin, ExportActionModelAdmin, admin.ModelAdmin
):
    resource_class = ProductoResource
    list_display = (
        'nombre', 'precio',
        'stock', 'compania', 'creado_por'
    )
