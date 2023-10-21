from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.http.response import JsonResponse

from . import models as m
from . import forms as f


class ListUsersView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView
):

    template_name = 'clientes/clientes_list.html'
    permission_required = 'organizaciones.pertenece_mesa_ayuda'


class ClienteDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):

    template_name = 'clientes/detail_cliente.html'
    permission_required = 'organizaciones.pertenece_mesa_ayuda'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    queryset = m.ClienteProfile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['cliente'] = profile
        return context


class AddClienteView(LoginRequiredMixin, PermissionRequiredMixin, generic.FormView):
    model = m.ClienteProfile
    form_class = f.AddNewCliente
    template_name = 'clientes/components/form_add_cliente.html'
    permission_required = 'integraciones.can_send_commands_mae'

    def form_valid(self, form):
        company = self.request.user.company_profile
        form.instance.company = company
        nombres = f'{form.instance.nombre} {form.instance.apellido}'
        form.save()
        cliente_id = form.instance.id

        if not form.instance.telefono or len(form.instance.telefono) != 10:
            form.add_error(
                None, 'Numero de telefono invalido.'
            )
            return self.form_invalid(form)

        success_url = reverse(
            'transacciones:transacciones_list', args=[cliente_id]
        )

        return JsonResponse(
            {
                'ok': True, 'transaction': 'Usuario', 'saldo': '',
                'user': nombres, 'successurl': success_url
            }
        )


class ClienteEditView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = m.ClienteProfile
    form_class = f.AddNewCliente
    template_name = 'clientes/components/form_add_cliente.html'
    permission_required = 'integraciones.can_send_commands_mae'

    def form_valid(self, form):
        nombres = f'{form.instance.nombre} {form.instance.apellido}'

        if not form.instance.telefono or len(form.instance.telefono) != 10:
            form.add_error(
                None, 'Numero de telefono invalido.'
            )
            return self.form_invalid(form)

        form.save()
        return JsonResponse({'ok': True, 'transaction': '', 'saldo': '', 'user': nombres})
