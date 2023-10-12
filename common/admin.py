from django.contrib import admin
from .models import ColombiaDepartments, ColombiaCities


@admin.register(ColombiaDepartments)
class ColombiaDepartmentsAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ColombiaCities)
class ColombiaCitiesAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']
