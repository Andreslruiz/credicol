from datetime import date, timedelta
from common.api_views import DataTablePagination, DataTableSearchFilter
from django.db.models import OuterRef, Subquery, Q
from rest_framework import permissions, generics, filters

from . import serializers as se
from .models import ClienteProfile
from transacciones.models import Transaccion


class ClientesFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        query = Q()
        estado = request.query_params.get('estado', None)

        if estado == 'en_mora':

            fecha_limite = date.today() - timedelta(days=15)

            ultima_transaccion_subquery = Transaccion.objects.filter(
                cliente=OuterRef('pk')
            ).order_by('-fecha_transaccion').values('fecha_transaccion')[:1]

            clientes_en_mora = ClienteProfile.objects.annotate(
                ultima_transaccion=Subquery(ultima_transaccion_subquery)
            ).filter(ultima_transaccion__lt=fecha_limite)

            fecha_limite = date.today() - timedelta(days=15)
            query &= Q(id__in=clientes_en_mora)

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
