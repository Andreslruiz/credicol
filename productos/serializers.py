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
        formatted_price = "{:,.0f}".format(total)
        return f"${formatted_price}"
