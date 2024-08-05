from django.contrib import admin
from .models import Gasto


@admin.register(Gasto)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['company', 'total_gasto', 'fecha_gasto']
