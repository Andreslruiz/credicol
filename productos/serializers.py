import locale

from rest_framework import serializers

from .models import Producto


class ProductosListSerializer(serializers.ModelSerializer):

    precio = serializers.SerializerMethodField()
    nombre = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = (
            'id',
            'nombre',
            'precio',
            'stock',
            'descripcion',
            'activo',
            'cantidad',
            'unidad_presentacion'
        )

    def get_precio(self, obj):
        total = abs(obj.precio)
        locale.setlocale(locale.LC_ALL, 'es_CO.utf8')
        total = locale._format("%d", total, grouping=True)
        return f'${total}'

    def get_nombre(self, obj):
        nombre = (
            f'{obj.nombre.title()} - {obj.cantidad} {obj.get_unidad_presentacion_display()}'
        )
        return nombre

    # def get_deuda(self, obj):
    #     deuda = obj.deuda
    #     return deuda
