from rest_framework import permissions, generics
from common.api_views import DataTablePagination, DataTableSearchFilter

from . import serializers as se
from .models import Reporte, Empleado


class ListarReportesAPIView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.ReportesListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DataTableSearchFilter]
    search_fields = ['cliente', 'tecnico__username', 'ciudad__name']

    def get_queryset(self):
        queryset = Reporte.objects.all().order_by('-fecha_creacion')
        return queryset


class ListarEmpleadosAPIView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.EmpleadosListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DataTableSearchFilter]
    search_fields = ['nombre', 'apellido']

    def get_queryset(self):
        queryset = Empleado.objects.all().order_by('-fecha_creacion')
        return queryset
