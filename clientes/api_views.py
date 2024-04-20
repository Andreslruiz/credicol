from rest_framework import permissions, generics
from common.api_views import DataTablePagination, DataTableSearchFilter

from . import serializers as se
from .models import ClienteProfile


class ListarClientesAPIView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.ClientesListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DataTableSearchFilter]
    search_fields = ['nombre', 'apellido']

    def get_queryset(self):
        queryset = ClienteProfile.objects.all()
        id = self.kwargs.get('company_id')
        if id:
            queryset = queryset.filter(company=id)

        return queryset
