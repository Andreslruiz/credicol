from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Reporte, Empleado


class ReportesListSerializer(serializers.ModelSerializer):
    tecnico = serializers.SerializerMethodField()
    fecha_creacion = serializers.SerializerMethodField()
    tipo_reporte = serializers.SerializerMethodField()
    ciudad = serializers.SerializerMethodField()

    class Meta:
        model = Reporte
        fields = (
            'id',
            'cliente',
            'ciudad',
            'tecnico',
            'tipo_reporte',
            'fecha_creacion'
        )

    def get_tecnico(self, obj):
        return obj.tecnico.username

    def get_tipo_reporte(self, obj):
        return obj.tipo_reporte.title()

    def get_ciudad(self, obj):
        return obj.ciudad.title()

    def get_fecha_creacion(self, obj):
        return obj.fecha_creacion.strftime('%d/%m/%Y %H:%M:%S')


class EmpleadosListSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    puesto = serializers.SerializerMethodField()

    class Meta:
        model = Empleado
        fields = (
            'id',
            'username',
            'nombre',
            'apellido',
            'telefono',
            'puesto',
            'fecha_creacion'
        )

    def get_nombre(self, obj):
        return f'{obj.nombre.title()} {obj.apellido.title()}'

    def get_puesto(self, obj):
        return obj.puesto.title()

    def get_username(self, obj):
        return obj.user.username
