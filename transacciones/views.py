from django.views import generic
from django.http.response import JsonResponse
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from . import models as m
from . import form as f
from . import services as s


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


class AddPaymentView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.FormView
):
    model = m.Transaccion
    form_class = f.AddPaymentForm
    template_name = 'transacciones/components/form_add_payment.html'
    permission_required = 'integraciones.can_send_commands_mae'

    def form_valid(self, form):
        cliente = s.get_cliente(self.kwargs.get('cliente_id'))
        total = form.instance.total_transaccion
        deuda = cliente.credit_balance

        if not cliente.telefono or len(cliente.telefono) != 10:
            form.add_error(
                None, 'Numero de telefono invalido, actualice la información del cliente.'
            )
            return self.form_invalid(form)

        if float(total) > float(deuda):
            form.add_error(
                None, f'El valor del pago es mayor a la deuda del usuario ${deuda}.'
            )
            return self.form_invalid(form)

        s.add_new_payment(form, cliente, self.request.user)
        deuda = cliente.deuda or '0'
        return JsonResponse({'ok': True, 'transaction': 'Pago', 'saldo': deuda})


class AddCreditView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.FormView
):
    model = m.Transaccion
    form_class = f.AddCreditForm
    template_name = 'transacciones/components/form_add_credit.html'
    permission_required = 'integraciones.can_send_commands_mae'

    def form_valid(self, form):
        cliente = s.get_cliente(self.kwargs.get('cliente_id'))

        if not cliente.telefono or len(cliente.telefono) != 10:
            form.add_error(
                None, 'Numero de telefono invalido, actualice la información del cliente.'
            )
            return self.form_invalid(form)

        s.add_new_credit(form, cliente, self.request.user)
        deuda = cliente.deuda

        return JsonResponse(
            {'ok': True, 'transaction': 'Fiado', 'saldo': deuda}
        )


class EditCreditView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView
):
    model = m.Transaccion
    form_class = f.AddCreditForm
    template_name = 'transacciones/components/form_add_credit.html'
    permission_required = 'integraciones.can_send_commands_mae'

    def form_valid(self, form):
        cliente = s.get_cliente(self.kwargs.get('cliente_id'))
        new_total = form.instance.total_transaccion

        if not cliente.telefono or len(cliente.telefono) != 10:
            form.add_error(
                None, 'Numero de telefono invalido, actualice la información del cliente.'
            )
            return self.form_invalid(form)

        s.update_last_credit(cliente, new_total, form)
        deuda = cliente.deuda

        return JsonResponse(
            {'ok': True, 'transaction': 'Fiado', 'saldo': deuda}
        )


class EditPaymentView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView
):
    model = m.Transaccion
    form_class = f.AddPaymentForm
    template_name = 'transacciones/components/form_add_payment.html'
    permission_required = 'integraciones.can_send_commands_mae'

    def form_valid(self, form):
        cliente = s.get_cliente(self.kwargs.get('cliente_id'))
        new_total = form.instance.total_transaccion

        if not cliente.telefono or len(cliente.telefono) != 10:
            form.add_error(
                None, 'Numero de telefono invalido, actualice la información del cliente.'
            )
            return self.form_invalid(form)

        s.update_last_payment(cliente, new_total, form)
        deuda = cliente.deuda

        return JsonResponse(
            {'ok': True, 'transaction': 'Fiado', 'saldo': deuda}
        )


class ListTransactionsView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView
):

    template_name = 'transacciones/transacciones_list.html'
    permission_required = 'organizaciones.pertenece_mesa_ayuda'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'cliente': s.get_cliente(self.kwargs.get('cliente_id'))
        })
        return super().get_context_data(**kwargs)
