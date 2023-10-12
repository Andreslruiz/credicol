from django.urls import path

from . import views

app_name = 'ventas'

urlpatterns = [
    path('direct-sales/', views.DirectSalesView.as_view(), name='direct_sales')
]
