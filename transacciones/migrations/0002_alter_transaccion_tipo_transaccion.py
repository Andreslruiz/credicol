# Generated by Django 4.2.5 on 2023-10-13 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transacciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaccion',
            name='tipo_transaccion',
            field=models.CharField(blank=True, choices=[('venta', 'Venta'), ('pago', 'Pago')], max_length=5, null=True),
        ),
    ]