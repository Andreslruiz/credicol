from rest_framework import serializers

from .models import ClienteProfile
from transacciones import services as tran_s


class ClientesListSerializer(serializers.ModelSerializer):

    telefono = serializers.SerializerMethodField()
    nombres = serializers.SerializerMethodField()
    deuda = serializers.SerializerMethodField()

    class Meta:
        model = ClienteProfile
        fields = (
            'id',
            'nombres',
            'email',
            'telefono',
            'deuda',
            'activo'
        )

    def get_telefono(self, obj):
        if obj.telefono != '0':
            telefono_limpio = ''.join(filter(str.isdigit, obj.telefono))
            return telefono_limpio

        return '-'

    def get_nombres(self, obj):
        nombres = f'{obj.nombre.title()} {obj.apellido.title()}'
        return nombres

    def get_deuda(self, obj):
        deuda = tran_s.get_current_user_deuda(obj)
        return deuda
