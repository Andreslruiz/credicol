from datetime import datetime, date
from unidecode import unidecode

from rest_framework import serializers

from .models import ClienteProfile
from transacciones.models import Transaccion


class ClientesListSerializer(serializers.ModelSerializer):

    telefono = serializers.SerializerMethodField()
    nombres = serializers.SerializerMethodField()
    deuda = serializers.SerializerMethodField()
    dias_mora = serializers.SerializerMethodField()

    class Meta:
        model = ClienteProfile
        fields = (
            'id',
            'nombres',
            'email',
            'telefono',
            'deuda',
            'activo',
            'dias_mora'
        )

    def get_telefono(self, obj):
        if obj.telefono != '0':
            telefono_limpio = ''.join(filter(str.isdigit, obj.telefono))
            return telefono_limpio

        return '-'

    def get_nombres(self, obj):
        nombres = f'{obj.nombre.title()} {obj.apellido.title()}'
        nombres = unidecode(nombres)
        return nombres

    def get_deuda(self, obj):
        deuda = obj.deuda
        return deuda

    def get_dias_mora(self, obj):
        return obj.dias_mora
