from rest_framework import permissions, generics
from common.api_views import DataTablePagination, DataTableSearchFilter

from . import serializers as se
from .models import Transaccion


class ListarTransaccionesAPIView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.TransaccionesListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DataTableSearchFilter]
    search_fields = ['id', 'id']

    def get_queryset(self):
        id = self.kwargs.get('cliente_id')
        queryset = Transaccion.objects.all()
        if id:
            queryset = queryset.filter(cliente=id).order_by('-id')

        return queryset
