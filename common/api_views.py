from rest_framework import pagination, response, filters, generics, permissions
from csp.decorators import csp_exempt

from . import models as m
from . import serializers as se


class DataTablePagination(pagination.LimitOffsetPagination):

    default_limit = 20
    offset_query_param = 'start'

    def get_paginated_response(self, data):
        return response.Response({
            'data': data,
            'recordsTotal': self.count,
            'recordsFiltered': self.count,
        })


class DataTableLongPagination(pagination.LimitOffsetPagination):

    default_limit = 1000
    offset_query_param = 'start'

    def get_paginated_response(self, data):
        return response.Response({
            'data': data,
            'recordsTotal': self.count,
            'recordsFiltered': self.count,
        })


class DataTablePaginationAutin(pagination.LimitOffsetPagination):

    default_limit = 'limit'
    offset_query_param = 'start'

    def get_paginated_response(self, data):
        return response.Response({
            'Total': self.count,
            'start': self.offset,
            'limit': self.limit,
            'data': data
        })


class DataTableSearchFilter(filters.SearchFilter):
    search_param = 'search[value]'


class InfoMunicipiosAPIView(generics.ListAPIView):

    serializer_class = se.MunicipiosSerializer
    filter_backends = [DataTableSearchFilter]
    search_fields = ['name', ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = m.ColombiaCities.objects.all()
        name = self.kwargs.get('name')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

    @csp_exempt
    def dispatch(self, *args, **kwargs):
        return super(InfoMunicipiosAPIView, self).dispatch(*args, **kwargs)
