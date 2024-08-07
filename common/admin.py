from django.contrib import admin
from .models import ColombiaDepartments, ColombiaCities, PendingMsgView
from import_export.admin import ImportExportMixin, ExportActionModelAdmin


@admin.register(ColombiaDepartments)
class ColombiaDepartmentsAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ColombiaCities)
class ColombiaCitiesAdmin(ImportExportMixin, ExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['name',]


@admin.register(PendingMsgView)
class PendingMsgViewAdmin(admin.ModelAdmin):
    list_display = ['url', 'type', 'error_code']
