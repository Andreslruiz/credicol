from django.contrib import admin
from import_export.admin import ImportExportMixin, ExportActionModelAdmin

from .models import ClienteProfile, MembresiaEmpresas
from .resources import ClienteProfileResource


@admin.register(ClienteProfile)
class CompanyProfileAdmin(
    ImportExportMixin, ExportActionModelAdmin, admin.ModelAdmin
):
    resource_class = ClienteProfileResource
    list_display = ['nombre', 'apellido', 'telefono', 'credit_balance']


@admin.register(MembresiaEmpresas)
class MembresiaEmpresasAdmin(
    ImportExportMixin, ExportActionModelAdmin, admin.ModelAdmin
):
    resource_class = MembresiaEmpresas
    list_display = ['empresa', 'dias_pagados', 'registrada_el', 'valor_pagado']
