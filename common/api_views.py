from rest_framework import pagination, response, filters


class DataTablePagination(pagination.LimitOffsetPagination):

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
