from datetime import datetime, timedelta
from rest_framework import permissions, generics, filters
from common.api_views import DataTablePagination, DataTableSearchFilter
from django.db.models import Q

from . import serializers as se
from .models import Gasto


class AllGastosFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        query = Q()
        date_range = request.query_params.get('rango_fecha', None)

        if date_range:
            date_range = date_range.replace('/', '-')
            date_range = date_range.split(' - ')

            start_date = datetime.strptime(date_range[0], "%Y-%m-%d")
            end_date = datetime.strptime(date_range[1], "%Y-%m-%d")
            end_date = end_date + timedelta(days=1) - timedelta(seconds=1)

            query = query & Q(fecha_gasto__range=[start_date, end_date])

        else:
            now = datetime.now()
            start_of_today = datetime(now.year, now.month, now.day)
            end_of_today = start_of_today + timedelta(days=1) - timedelta(seconds=1)
            query = query & Q(fecha_gasto__range=[start_of_today, end_of_today])

        return queryset.filter(query)


class ListarAllGastosAPIView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.GastosListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DataTableSearchFilter, AllGastosFilter]
    search_fields = ['id']

    def get_queryset(self):
        company = self.request.user.company_profile
        queryset = Gasto.objects.filter(company=company)
        return queryset
