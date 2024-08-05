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
    permission_required = 'transacciones.can_see_cliente_transacciones'


class AddProductoView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.FormView
):
    model = m.Producto
    form_class = f.AddNewProducto
    template_name = 'productos/components/form_add_producto.html'
    permission_required = 'transacciones.can_see_cliente_transacciones'

    def post(self, request, *args, **kwargs):
        modified_post_data = request.POST.copy()
        for field, value in modified_post_data.items():
            modified_post_data[field] = value.replace('.', '')
            if not value:
                modified_post_data[field] = 0

        form = self.get_form_class()(data=modified_post_data)

        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        product = form.instance.nombre
        compania = self.request.user.company_profile
        form.instance.compania = compania
        form.save(self.request.user)

        return JsonResponse(
            {
                'ok': True, 'product': product, 'label': 'Registrado'
            }
        )


class EditarProductoView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView
):
    model = m.Producto
    form_class = f.AddNewProducto
    template_name = 'productos/components/form_add_producto.html'
    permission_required = 'transacciones.can_see_cliente_transacciones'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        modified_post_data = request.POST.copy()
        for field, value in modified_post_data.items():
            modified_post_data[field] = value.replace('.', '')
            if not value:
                modified_post_data[field] = 0

        form = self.get_form_class()(data=modified_post_data, instance=self.object)

        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        product = form.instance.nombre
        compania = self.request.user.company_profile
        form.instance.compania = compania
        form.save(self.request.user)

        return JsonResponse(
            {
                'ok': True, 'product': product, 'label': 'Actualizado'
            }
        )


class DetailProductoView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView
):
    model = m.Producto
    template_name = 'productos/components/detalle_producto.html'
    permission_required = 'transacciones.can_see_cliente_transacciones'
