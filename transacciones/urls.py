from django.urls import path

from . import api_views
from . import views

app_name = 'transacciones'

urlpatterns = [
    path('direct-sales/', views.DirectSalesView.as_view(), name='direct_sales'),
    path('close-day', views.CloseDayView.as_view(), name='close_day'),
    path(
        'add-payment/<int:cliente_id>', views.AddPaymentView.as_view(),
        name='add_payment'
    ),
    path(
        'add-credit/<int:cliente_id>', views.AddCreditView.as_view(),
        name='add_credit'
    ),
    path(
        'edit-credit/<int:pk>/<int:cliente_id>', views.EditCreditView.as_view(),
        name='edit_credit'
    ),
    path(
        'edit-payment/<int:pk>/<int:cliente_id>', views.EditPaymentView.as_view(),
        name='edit_payment'
    ),
    path(
        'edit-transaction/<int:pk>/', views.EditTransactionView.as_view(),
        name='edit_transaction'
    ),
    path(
        'delete-transaction/<int:pk>/', views.delete_transaction,
        name='delete_transaction'
    ),
    path(
        'detalle/<int:cliente_id>',
        views.ListTransactionsView.as_view(),
        name='transacciones_list'
    ),
    path(
        'api/transacciones/<int:cliente_id>',
        api_views.ListarTransaccionesAPIView.as_view(),
        name='listar_transacciones_api'
    ),
    path(
        '',
        views.ListAllTransactionsView.as_view(),
        name='full_transacciones_list'
    ),
    path(
        'api/transacciones/',
        api_views.ListarAllTransaccionesAPIView.as_view(),
        name='listar_all_transacciones_api'
    ),
    path(
        'remember-payment/<int:cliente_id>',
        views.recordar_deuda,
        name='remember_payment'
    )
]
