import locale

from rest_framework import serializers

from .models import Transaccion


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
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_formateada = obj.fecha_transaccion.strftime(
            '%d de %B de %Y, %H:%M:%S'
        ).title()
        locale.setlocale(locale.LC_TIME, '')
        return fecha_formateada
