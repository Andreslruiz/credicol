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
        fecha_actual = date.today()
        deuda = obj.deuda
        transacciones = Transaccion.objects.filter(cliente=obj)
        deuda_clean = ''.join(c for c in deuda if c.isdigit())

        if int(deuda_clean) > 0 and transacciones:
            tr = Transaccion.objects.filter(cliente=obj).order_by('-fecha_transaccion').first()
            ultimo_pago = tr.fecha_transaccion

            if isinstance(ultimo_pago, datetime):
                ultimo_pago = ultimo_pago.date()

            diferencia = fecha_actual - ultimo_pago

            dias_pasados = diferencia.days

        else:
            dias_pasados = 0

        if dias_pasados > 0:
            return dias_pasados

        return ''
