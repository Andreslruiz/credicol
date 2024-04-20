import locale
from datetime import datetime

from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
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

        if form.instance.total_transaccion <= 0:
            form.add_error(
                None, 'El total debe de ser un numero entero y positivo.'
            )
            return self.form_invalid(form)

        form.instance.creada_por = self.request.user
        form.instance.tipo_transaccion = m.Transaccion.TIPO_CHOICES[0][0]
        form.instance.observaciones = 'Venta Rapida'
        form.save()

        total = f'{form.instance.total_transaccion:,.0f}'

        return JsonResponse(
            {'ok': True, 'transaction': 'Venta Registrada', 'value': total}
        )


class AddPaymentView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.FormView
):
    model = m.Transaccion
    form_class = f.AddPaymentForm
    template_name = 'transacciones/components/form_add_payment.html'
    permission_required = 'transacciones.can_add_transaccion'

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
    permission_required = 'transacciones.can_add_transaccion'

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
            {'ok': True, 'transaction': 'Fiado Registrado', 'saldo': deuda}
        )


class EditCreditView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView
):
    model = m.Transaccion
    form_class = f.AddCreditForm
    template_name = 'transacciones/components/form_add_credit.html'
    permission_required = 'transacciones.can_edit_transaccion'

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
            {'ok': True, 'transaction': 'Fiado Actualizado', 'saldo': deuda}
        )


class EditPaymentView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView
):
    model = m.Transaccion
    form_class = f.AddPaymentForm
    template_name = 'transacciones/components/form_add_payment.html'
    permission_required = 'transacciones.can_edit_transaccion'

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
            {'ok': True, 'transaction': 'Pago Actualizado', 'saldo': deuda}
        )


class EditTransactionView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView
):
    model = m.Transaccion
    form_class = f.EditTransactionForm
    template_name = 'transacciones/components/form_edit_transaction.html'
    permission_required = 'transacciones.can_edit_transaccion'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'actual_transaction': self.object.id
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        new_total = form.instance.total_transaccion

        s.update_last_transaction(new_total, form, self.kwargs.get('pk'))

        locale.setlocale(locale.LC_ALL, 'es_CO.utf8')
        total = locale._format("%d", new_total, grouping=True)

        return JsonResponse(
                {'ok': True, 'transaction': 'Transacción Actualizada', 'value': total}
        )


def delete_transaction(request, pk):
    s.delete_last_transaction(pk)
    return JsonResponse(
        {'ok': True}
    )


class ListTransactionsView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView
):

    template_name = 'transacciones/transacciones_list.html'
    permission_required = 'transacciones.can_see_cliente_transacciones'

    def get_context_data(self, **kwargs):
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%Y-%m-%d %H:%M')
        kwargs.update({
            'cliente': s.get_cliente(self.kwargs.get('cliente_id')),
            'fecha_actual': fecha_formateada
        })
        return super().get_context_data(**kwargs)


class ListAllTransactionsView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView
):

    template_name = 'transacciones/all_transacciones_list.html'
    permission_required = 'organizaciones.pertenece_mesa_ayuda'

    def get_context_data(self, **kwargs):
        kwargs.update({
            # 'cliente': s.get_cliente(self.kwargs.get('cliente_id'))
        })
        return super().get_context_data(**kwargs)
