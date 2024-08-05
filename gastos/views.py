from django.views import generic
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.utils import timezone
from django.http.response import JsonResponse

from . import models as m
from . import forms as f


class ListAllGastosView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView
):

    template_name = 'gastos/all_gastos_list.html'
    permission_required = 'gastos.can_edit_gasto'

    def get_context_data(self, **kwargs):
        kwargs.update({
            # 'cliente': s.get_cliente(self.kwargs.get('cliente_id'))
        })
        return super().get_context_data(**kwargs)


class AddGastoView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView
):
    model = m.Gasto
    form_class = f.CrearGastoForm
    template_name = 'gastos/components/add_gasto.html'
    permission_required = 'gastos.can_add_gasto'

    def form_valid(self, form):

        if form.instance.total_gasto <= 0:
            form.add_error(
                None, 'El total debe de ser un numero entero y positivo.'
            )
            return self.form_invalid(form)

        form.instance.creada_por = self.request.user
        form.instance.company = self.request.user.company_profile
        form.instance.fecha_gasto = timezone.now()
        form.save()

        total = f'{form.instance.total_gasto:,.0f}'

        return JsonResponse(
            {'ok': True, 'transaction': 'Gasto Registrado', 'value': total}
        )


class EditGastoView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView
):
    model = m.Gasto
    form_class = f.CrearGastoForm
    template_name = 'gastos/components/add_gasto.html'
    permission_required = 'gastos.can_add_gasto'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'actual_gasto': self.object.id
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):

        if form.instance.total_gasto <= 0:
            form.add_error(
                None, 'El total debe de ser un numero entero y positivo.'
            )
            return self.form_invalid(form)

        form.instance.creada_por = self.request.user
        form.save()

        total = f'{form.instance.total_gasto:,.0f}'

        return JsonResponse(
            {'ok': True, 'transaction': 'Gasto Actualizado', 'value': total}
        )
