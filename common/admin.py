from django.contrib import admin
from .models import ColombiaDepartments, ColombiaCities, PendingMsgView


@admin.register(ColombiaDepartments)
class ColombiaDepartmentsAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ColombiaCities)
class ColombiaCitiesAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']


@admin.register(PendingMsgView)
class PendingMsgViewAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'text', 'error_code']
