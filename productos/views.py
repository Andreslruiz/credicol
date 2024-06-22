from django.views import generic
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.urls import reverse
from django.http.response import JsonResponse

from . import models as m
from . import forms as f


class ListProductosView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView
):

    template_name = 'productos/productos_list.html'
    permission_required = 'organizaciones.pertenece_mesa_ayuda'


class AddProductoView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.FormView
):
    model = m.Producto
    form_class = f.AddNewProducto
    template_name = 'productos/components/form_add_producto.html'
    permission_required = 'integraciones.can_send_commands_mae'

    def form_valid(self, form):
        product = form.instance.nombre
        compania = self.request.user.company_profile
        form.instance.compania = compania
        form.save(self.request.user)

        return JsonResponse(
            {
                'ok': True, 'product': product
            }
        )
