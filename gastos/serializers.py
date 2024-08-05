from django.utils import timezone
import locale

from rest_framework import serializers

from .models import Gasto


class GastosListSerializer(serializers.ModelSerializer):

    total_gasto = serializers.SerializerMethodField()
    creada_por = serializers.SerializerMethodField()
    fecha_gasto = serializers.SerializerMethodField()
    observaciones = serializers.SerializerMethodField()

    class Meta:
        model = Gasto
        fields = (
            'id',
            'observaciones',
            'total_gasto',
            'fecha_gasto',
            'creada_por',
        )

    def get_total_gasto(self, obj):
        total = abs(obj.total_gasto)
        total_formateado = "{:,.0f}".format(int(total))
        return "${}".format(total_formateado)

    def get_creada_por(self, obj):
        nombres = f'{obj.creada_por.first_name.title()} {obj.creada_por.last_name.title()}'
        return nombres

    def get_observaciones(self, obj):
        return obj.observaciones.title()

    def get_fecha_gasto(self, obj):
        fecha_local = timezone.localtime(obj.fecha_gasto)

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_formateada = fecha_local.strftime('%d de %B de %Y, %H:%M:%S')

        locale.setlocale(locale.LC_TIME, '')

        return fecha_formateada
