from django.contrib import admin
from .models import CompanyProfile, CierreCaja, Proprietario


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']


@admin.register(CierreCaja)
class CierreCajaAdmin(admin.ModelAdmin):
    list_display = ['compania', 'total_credito', 'total_efectivo']


@admin.register(Proprietario)
class ProprietarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'email']
