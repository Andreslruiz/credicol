from django.contrib import admin
from import_export.admin import ImportExportMixin, ExportActionModelAdmin

from .models import ClienteProfile
from .resources import ClienteProfileResource


@admin.register(ClienteProfile)
class CompanyProfileAdmin(
    ImportExportMixin, ExportActionModelAdmin, admin.ModelAdmin
):
    resource_class = ClienteProfileResource
    list_display = ['nombre', 'apellido', 'telefono', 'credit_balance']
