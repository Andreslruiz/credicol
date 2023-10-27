from import_export import resources, fields
from import_export.widgets import DateTimeWidget

from .models import ClienteProfile


class ClienteProfileResource(resources.ModelResource):

    fecha_registro = fields.Field(
        column_name='fecha_registro',
        attribute='fecha_registro',
        widget=DateTimeWidget(format='%d/%m/%Y')
    )

    class Meta:
        model = ClienteProfile
