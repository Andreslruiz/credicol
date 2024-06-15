from datetime import datetime, timedelta
from rest_framework import permissions, generics, filters
from common.api_views import DataTablePagination, DataTableSearchFilter
from django.db.models import Q

from . import serializers as se
from .models import Transaccion


class ListarTransaccionesAPIView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.TransaccionesListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DataTableSearchFilter]
    search_fields = ['id']

    def get_queryset(self):
        id = self.kwargs.get('cliente_id')
        queryset = Transaccion.objects.all()
        if id:
            queryset = queryset.filter(cliente=id).order_by('-id')

        return queryset


class AllTransactionsFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        query = Q()
        date_range = request.query_params.get('rango_fecha', None)

        if date_range:
            date_range = date_range.replace('/', '-')
            date_range = date_range.split(' - ')

            start_date = datetime.strptime(date_range[0], "%Y-%m-%d")
            end_date = datetime.strptime(date_range[1], "%Y-%m-%d")
            end_date = end_date + timedelta(days=1) - timedelta(seconds=1)

            query = query & Q(fecha_transaccion__range=[start_date, end_date])

        else:
            now = datetime.now()
            start_of_today = datetime(now.year, now.month, now.day)
            end_of_today = start_of_today + timedelta(days=1) - timedelta(seconds=1)
            query = query & Q(fecha_transaccion__range=[start_of_today, end_of_today])

        return queryset.filter(query)


class ListarAllTransaccionesAPIView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.TransaccionesListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DataTableSearchFilter, AllTransactionsFilter]
    search_fields = ['id']

    def get_queryset(self):
        queryset = Transaccion.objects.all().order_by('-id')
        return queryset
