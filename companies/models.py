from django.db import models
from simple_history.models import HistoricalRecords
from django.utils import timezone
from django.conf import settings


class CompanyProfile(models.Model):
    profile_photo = models.FileField(upload_to='companies/', blank=True, null=True)
    name = models.CharField(max_length=200)
    nit = models.CharField(max_length=200)
    slogan = models.CharField(max_length=300)
    city = models.ForeignKey('common.ColombiaCities', on_delete=models.CASCADE)
    email = models.EmailField()
    contact = models.CharField(max_length=200)
    code = models.IntegerField(blank=True, default=0)
    login_attemps = models.IntegerField(blank=True, default=0)
    date_password_updated = models.DateTimeField(default=timezone.now)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='company_profile',
        on_delete=models.CASCADE
    )
    fin_fecha_membresia = models.DateTimeField(blank=True, null=True)
    envio_mensajes = models.BooleanField(default=False)
    propietario = models.ForeignKey(
        'companies.Proprietario', on_delete=models.CASCADE, related_name='propietario',
        blank=True, null=True
    )

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name} - {self.city.name}'


class CierreCaja(models.Model):
    compania = models.ForeignKey('companies.CompanyProfile', on_delete=models.CASCADE, related_name='cierres_caja')
    fecha = models.DateTimeField(auto_now_add=True)
    total_credito = models.PositiveIntegerField(default=0)
    total_efectivo = models.PositiveIntegerField(default=0)
    total_gastos = models.PositiveIntegerField(default=0)
    comentarios = models.TextField(blank=True, null=True)
    cerrada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Cierre de Caja'
        verbose_name_plural = 'Cierres de Caja'

    def __str__(self):
        return f"Cierre de Caja - {self.compania.name} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"


class Proprietario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proprietor_profile')
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Propietario'
        verbose_name_plural = 'Propietarios'
