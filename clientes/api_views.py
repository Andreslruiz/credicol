from datetime import date, timedelta
from rest_framework import permissions, generics
from common.api_views import DataTablePagination, DataTableSearchFilter
from django.db.models import Q
from rest_framework import permissions, generics, filters

from . import serializers as se
from .models import ClienteProfile


class ClientesFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        query = Q()
        estado = request.query_params.get('estado', None)

        if estado == 'en_mora':
            fecha_limite = date.today() - timedelta(days=15)
            query &= Q(transacciones_cliente__fecha_transaccion__lt=fecha_limite)

        if estado == 'al_dia':
            fecha_limite = date.today() - timedelta(days=15)
            query &= (
                Q(transacciones_cliente__fecha_transaccion__gt=fecha_limite) |
                Q(credit_balance=0) |
                Q(credit_balance__isnull=True)
            )

        return queryset.filter(query).distinct()


class ListarClientesAPIView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.ClientesListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DataTableSearchFilter, ClientesFilter]
    search_fields = ['nombre', 'apellido']

    def get_queryset(self):
        queryset = ClienteProfile.objects.all().order_by('-credit_balance')
        id = self.kwargs.get('company_id')
        if id:
            queryset = queryset.filter(company=id)

        return queryset
