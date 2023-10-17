from django.urls import path

from . import views

app_name = 'transacciones'

urlpatterns = [
    path('direct-sales/', views.DirectSalesView.as_view(), name='direct_sales'),
    path(
        'add-payment/<int:cliente_id>', views.AddPaymentView.as_view(),
        name='add_payment'
    ),
    path(
        'add-credit/<int:cliente_id>', views.AddCreditView.as_view(),
        name='add_credit'
    ),
]
