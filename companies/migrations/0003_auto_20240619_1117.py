# Generated by Django 3.2.8 on 2024-06-19 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_auto_20240423_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyprofile',
            name='envio_mensajes',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalcompanyprofile',
            name='envio_mensajes',
            field=models.BooleanField(default=False),
        ),
    ]
