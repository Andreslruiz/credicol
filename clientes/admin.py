from django.contrib import admin
from .models import ClienteProfile


@admin.register(ClienteProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'telefono']
