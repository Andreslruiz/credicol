import locale

from rest_framework import serializers

from .models import Transaccion


class TransaccionesListSerializer(serializers.ModelSerializer):

    total_transaccion = serializers.SerializerMethodField()
    creada_por = serializers.SerializerMethodField()
    fecha_transaccion = serializers.SerializerMethodField()
    observaciones = serializers.SerializerMethodField()

    class Meta:
        model = Transaccion
        fields = (
            'id',
            'total_transaccion',
            'fecha_transaccion',
            'creada_por',
            'tipo_transaccion',
            'es_fiado',
            'observaciones'
        )

    def get_total_transaccion(self, obj):
        total = abs(obj.total_transaccion)
        # locale.setlocale(locale.LC_ALL, 'es_CO.utf8')
        # total = locale._format("%d", total, grouping=True)
        return f'${total}'

    def get_creada_por(self, obj):
        nombres = f'{obj.creada_por.first_name} {obj.creada_por.last_name}'
        return nombres

    def get_observaciones(self, obj):
        return obj.observaciones.title()

    def get_fecha_transaccion(self, obj):
        return obj.fecha_transaccion.strftime(
            '%A, %d de %B de %Y, %H:%M:%S'
        ).title()
