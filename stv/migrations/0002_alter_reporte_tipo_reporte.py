# Generated by Django 3.2.8 on 2024-08-06 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stv', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte',
            name='tipo_reporte',
            field=models.CharField(blank=True, choices=[('preventivo', 'Preventivo'), ('reparacion', 'Reparación'), ('correctivo', 'Correctivo'), ('inspeccion_norma', 'Inspección Norma')], max_length=20, null=True),
        ),
    ]