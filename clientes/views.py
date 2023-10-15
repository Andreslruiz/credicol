from django.views import generic
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from . import models as m
from transacciones.services import get_current_user_deuda

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
        context['total_deuda'] = get_current_user_deuda(profile)
        return context
