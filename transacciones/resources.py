from import_export import resources
from .models import Transaccion


class TransaccionesResource(resources.ModelResource):
    class Meta:
        model = Transaccion
