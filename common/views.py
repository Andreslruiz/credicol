from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.contrib.auth import get_user_model


from transacciones.services import (
    get_sales_month, get_sales_year, get_sales_today,
    get_all_year_sales
)
from . import services as s

User = get_user_model()


class LoginUsuario(LoginView):
    """
    Custom login view.
    """
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = '/dashboard/'

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


class InitialView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView
):

    template_name = 'common/initial.html'
    permission_required = 'common.can_see_initial_view'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'user': self.request.user.company_profile,
            'sales_last_month': get_sales_month(self.request.user),
            'sales_last_year': get_sales_year(self.request.user),
            'sales_today': get_sales_today(self.request.user),
            'sales_all_year': get_all_year_sales(self.request.user)
        })
        return super().get_context_data(**kwargs)


def user_logout(request):
    logout(request)
    return redirect(reverse('login'))


def send_daily_report(request):
    s.send_daily_report(request.user)
    return redirect(reverse('initial_view'))
