from django.urls import path

from . import views

app_name = 'common'

urlpatterns = [
    path('deone/', views.DeOneView.as_view(), name='deone_main'),
    path('dashboard', views.DashBoardSalesView.as_view(), name='dashboard_sales')
]
