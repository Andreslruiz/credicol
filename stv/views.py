import os

from django.conf import settings
from django.views import generic
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.db import transaction
from django.http.response import JsonResponse
from django.http import FileResponse, Http404
from django.shortcuts import resolve_url
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from .models import Reporte
from . import forms as f
from . import services as s

User = get_user_model()


class InitialStvView(generic.TemplateView):

    template_name = 'stv/initial.html'
    permission_required = 'stv.can_see_initial_view'


class LoginStvUser(LoginView):
    template_name = 'stv/login_stv.html'
    redirect_authenticated_user = True
    success_url = 'stv:report_list'

    def form_invalid(self, form):

        try:
            self.usuario = User.objects.get(
                username=self.request.POST['username']
            )
        except Exception:
            return super().form_invalid(form)

        return super().form_invalid(form)

    def form_valid(self, form):

        try:
            self.usuario = form.get_user()
        except Exception:
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return resolve_url(self.success_url)


class ListReportsView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView
):

    template_name = 'stv/report_list.html'
    permission_required = 'stv.can_see_reports'


class AddReportView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView
):
    model = Reporte
    form_class = f.AddNewReport
    template_name = 'stv/components/form_add_report.html'
    permission_required = 'stv.can_upload_reports'

    def form_valid(self, form):
        form.save(self.request.user)
        cliente = form.instance.cliente.title()
        s.create_new_report(form.instance, self.request)
        return JsonResponse(
            {
                'ok': True, 'product': cliente, 'label': 'creado'
            }
        )


def download_report(request, id):
    with transaction.atomic():
        try:
            report = Reporte.objects.get(id=id)
            file_name = report.archivo.name
            file_path = f'{settings.MEDIA_ROOT}/reportes/{file_name}'

            if not os.path.exists(file_path):
                raise Http404("Archivo no encontrado.")

            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
            return response

        except Reporte.DoesNotExist:
            raise Http404("Reporte no encontrado.")
