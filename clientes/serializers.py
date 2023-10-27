from unidecode import unidecode

from rest_framework import serializers

from .models import ClienteProfile


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
        nombres = unidecode(nombres)
        return nombres

    def get_deuda(self, obj):
        deuda = obj.deuda
        return deuda
