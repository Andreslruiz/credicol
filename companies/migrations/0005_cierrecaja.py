# Generated by Django 3.2.8 on 2024-06-29 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0004_auto_20240624_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='CierreCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total_credito', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_efectivo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_gastos', models.DecimalField(decimal_places=2, max_digits=10)),
                ('comentarios', models.TextField(blank=True, null=True)),
                ('cerrada_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('compania', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cierres_caja', to='companies.companyprofile')),
            ],
            options={
                'verbose_name': 'Cierre de Caja',
                'verbose_name_plural': 'Cierres de Caja',
                'ordering': ['-fecha'],
            },
        ),
    ]