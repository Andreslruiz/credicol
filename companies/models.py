from django.db import models
from simple_history.models import HistoricalRecords
from django.utils import timezone
from django.conf import settings


class CompanyProfile(models.Model):
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

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name} - {self.city.name}'
