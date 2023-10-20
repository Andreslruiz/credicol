from django.views import generic
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)


class ListProductosView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView
):

    template_name = 'productos/productos_list.html'
    permission_required = 'organizaciones.pertenece_mesa_ayuda'
