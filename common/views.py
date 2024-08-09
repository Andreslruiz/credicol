from django.contrib.auth import logout, login
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.contrib.auth import get_user_model

from transacciones.services import (
    get_sales_month, get_sales_year, get_sales_today,
    get_all_year_sales, total_credit_amount, get_credit_sales_today,
    get_today_payments, get_today_gastos
)
from .forms import RegisterForm
from . import selectors as sel
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
    permission_required = 'clientes.can_see_initial_view'

    def get_context_data(self, **kwargs):
        today_sales = get_sales_today(self.request.user)
        today_credit_sales = get_credit_sales_today(self.request.user)
        today_add_payment = get_today_payments(self.request.user)
        today_gastos = get_today_gastos(self.request.user)
        total_today = int(today_sales.replace(",", "")) + int(today_add_payment.replace(",", "")) - int(today_gastos.replace(",", ""))

        kwargs.update({
            'user': self.request.user.company_profile,
            'sales_last_month': get_sales_month(self.request.user),
            'sales_last_year': get_sales_year(self.request.user),
            'sales_today': today_sales,
            'sales_credit_today': today_credit_sales,
            'today_payments': today_add_payment,
            'today_gastos': today_gastos,
            'total_today': f'{total_today:,.0f}',
            'sales_all_year': get_all_year_sales(self.request.user),
            'total_credit_amount': total_credit_amount(
                self.request.user.company_profile
            ),
            'day_closed': sel.get_today_close(self.request.user.company_profile)
        })
        return super().get_context_data(**kwargs)


class DeOneView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView
):

    template_name = 'common/deone.html'
    permission_required = 'clientes.can_see_initial_view'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'user': self.request.user.company_profile,
            'sales_last_month': get_sales_month(self.request.user),
            'sales_last_year': get_sales_year(self.request.user),
            'sales_today': get_sales_today(self.request.user),
            'sales_all_year': get_all_year_sales(self.request.user),
            'total_credit_amount': total_credit_amount(
                self.request.user.company_profile
            )
        })
        return super().get_context_data(**kwargs)


def user_logout(request, origin):
    logout(request)

    if origin == 'stv':
        return redirect('stv:stv_login')

    return redirect(reverse('login'))


class DashBoardSalesView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView
):

    template_name = 'common/dashboard_sales.html'
    permission_required = 'clientes.can_see_initial_view'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'products': sel.get_company_products(self.request.user),
        })
        return super().get_context_data(**kwargs)


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = '/dashboard/'

    def form_valid(self, form):
        user = form.save()
        country_code = self.request.POST.get('country')
        phone_number = self.request.POST.get('phone_number')
        company_name = self.request.POST.get('company_name')
        company_logo = self.request.FILES.get('company_logo')

        try:
            s.create_company_profile(company_name, user, country_code, phone_number, company_logo)
            login(self.request, user)
        except Exception as e:
            user.delete()
            form.add_error('username', e)
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url
