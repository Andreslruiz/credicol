from import_export import resources, fields
from import_export.widgets import DateTimeWidget

from .models import Transaccion


class TransaccionesResource(resources.ModelResource):

    fecha_transaccion = fields.Field(
        column_name='fecha_transaccion',
        attribute='fecha_transaccion',
        widget=DateTimeWidget(format='%d/%m/%Y')
    )

    class Meta:
        model = Transaccion
