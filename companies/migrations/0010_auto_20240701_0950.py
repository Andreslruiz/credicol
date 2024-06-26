# Generated by Django 3.2.8 on 2024-07-01 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0009_auto_20240701_0922'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyprofile',
            name='users',
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcompanyprofile',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
