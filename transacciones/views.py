from django.views import generic
from django.http.response import JsonResponse
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from . import models as m
from . import form as f


class DirectSalesView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView
):
    model = m.Transaccion
    form_class = f.CrearVentaForm
    template_name = 'transacciones/components/direct_sales.html'
    permission_required = 'transmision.can_admin_direccionamiento'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'active': 'si'
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # com_s.send_daily_notification(form.instance.total_venta)
        form.instance.usuario = self.request.user
        form.instance.tipo_transaccion = m.Transaccion.TIPO_CHOICES[0][0]
        form.save()
        return JsonResponse({'ok': True})
