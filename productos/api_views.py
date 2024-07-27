from rest_framework import permissions, generics
from common.api_views import DataTablePagination, DataTableSearchFilter

from . import serializers as se
from .models import Producto


class ListarProductosAPIView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.ProductosListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DataTableSearchFilter]
    search_fields = ['nombre', 'descripcion']

    def get_queryset(self):
        id = self.kwargs.get('producto_id')
        company = self.request.user.company_profile
        queryset = Producto.objects.filter(creado_por__company_profile=company).order_by('-fecha_creacion')
        if id:
            queryset = queryset.filter(compania=1)

        return queryset
