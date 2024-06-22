import locale

from rest_framework import serializers

from .models import Producto


class ProductosListSerializer(serializers.ModelSerializer):

    precio = serializers.SerializerMethodField()
    precio_venta = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = (
            'id',
            'nombre',
            'precio',
            'stock',
            'descripcion',
            'activo',
            'precio_venta'
        )

    def get_precio(self, obj):
        total = abs(obj.precio)
        formatted_price = "{:,.0f}".format(total)
        return f"${formatted_price}"

    def get_precio_venta(self, obj):
        total = abs(obj.precio_venta)
        formatted_price = "{:,.0f}".format(total)
        return f"${formatted_price}"
