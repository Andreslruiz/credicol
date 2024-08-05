from django.utils import timezone
import locale

from rest_framework import serializers

from .models import Transaccion
from companies.models import CierreCaja


class CierresListSerializer(serializers.ModelSerializer):

    total_credito = serializers.SerializerMethodField()
    total_efectivo = serializers.SerializerMethodField()
    total_gastos = serializers.SerializerMethodField()
    cerrada_por = serializers.SerializerMethodField()
    fecha = serializers.SerializerMethodField()
    comentarios = serializers.SerializerMethodField()

    class Meta:
        model = CierreCaja
        fields = (
            'id',
            'fecha',
            'total_credito',
            'total_efectivo',
            'total_gastos',
            'comentarios',
            'cerrada_por'
        )

    def get_total_credito(self, obj):
        total = abs(obj.total_credito)
        total_formateado = "{:,.0f}".format(int(total))
        return "${}".format(total_formateado)

    def get_total_efectivo(self, obj):
        total = abs(obj.total_efectivo)
        total_formateado = "{:,.0f}".format(int(total))
        return "${}".format(total_formateado)

    def get_total_gastos(self, obj):
        total = abs(obj.total_gastos)
        total_formateado = "{:,.0f}".format(int(total))
        return "${}".format(total_formateado)

    def get_cerrada_por(self, obj):
        nombres = f'{obj.cerrada_por.first_name.title()} {obj.cerrada_por.last_name.title()}'
        return nombres

    def get_comentarios(self, obj):
        return obj.comentarios.title()

    def get_fecha(self, obj):
        fecha_local = timezone.localtime(obj.fecha)

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_formateada = fecha_local.strftime('%d de %B de %Y, %H:%M:%S')

        locale.setlocale(locale.LC_TIME, '')

        return fecha_formateada


class TransaccionesListSerializer(serializers.ModelSerializer):

    total_transaccion = serializers.SerializerMethodField()
    creada_por = serializers.SerializerMethodField()
    fecha_transaccion = serializers.SerializerMethodField()
    observaciones = serializers.SerializerMethodField()
    cliente = serializers.SerializerMethodField()

    class Meta:
        model = Transaccion
        fields = (
            'id',
            'cliente',
            'total_transaccion',
            'fecha_transaccion',
            'creada_por',
            'tipo_transaccion',
            'es_fiado',
            'observaciones'
        )

    def get_total_transaccion(self, obj):
        total = abs(obj.total_transaccion)
        total_formateado = "{:,.0f}".format(int(total))
        return "${}".format(total_formateado)

    def get_creada_por(self, obj):
        nombres = f'{obj.creada_por.first_name.title()} {obj.creada_por.last_name.title()}'
        return nombres

    def get_cliente(self, obj):
        if obj.cliente:
            return f'{obj.cliente.nombre.title()} {obj.cliente.apellido.title()}'
        return '-'

    def get_observaciones(self, obj):
        return obj.observaciones.title()

    def get_fecha_transaccion(self, obj):
        fecha_local = timezone.localtime(obj.fecha_transaccion)

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_formateada = fecha_local.strftime('%d de %B de %Y, %H:%M:%S')

        locale.setlocale(locale.LC_TIME, '')

        return fecha_formateada
