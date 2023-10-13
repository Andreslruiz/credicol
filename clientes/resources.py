from import_export import resources
from .models import ClienteProfile


class ClienteProfileResource(resources.ModelResource):
    class Meta:
        model = ClienteProfile
