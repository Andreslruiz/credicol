from typing import Any
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.contrib.auth import get_user_model

from ventas.services import get_sales_month, get_sales_year, get_sales_today

User = get_user_model()


class LoginUsuario(LoginView):
    """
    Custom login view.
    """
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = '/admin/'

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
        return self.success_url


class InitialView(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):

    template_name = 'common/initial.html'
    permission_required = 'common.can_see_initial_view'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'user': self.request.user.company_profile,
            'sales_last_month': get_sales_month(self.request.user),
            'sales_last_year': get_sales_year(self.request.user),
            'sales_today': get_sales_today(self.request.user)
        })
        return super().get_context_data(**kwargs)
