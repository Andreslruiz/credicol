import locale

from rest_framework import serializers

from .models import Producto


class ProductosListSerializer(serializers.ModelSerializer):

    precio = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = (
            'id',
            'nombre',
            'precio',
            'stock',
            'descripcion',
            'activo',
        )

    def get_precio(self, obj):
        total = abs(obj.precio)
        locale.setlocale(locale.LC_ALL, 'es_CO.utf8')
        total = locale._format("%d", total, grouping=True)
        return f'${total}'
