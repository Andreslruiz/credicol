from django.urls import path

from . import views
from . import api_views

app_name = 'common'

urlpatterns = [
    path('deone/', views.DeOneView.as_view(), name='deone_main'),
    path('dashboard', views.DashBoardSalesView.as_view(), name='dashboard_sales'),
    path(
        'api/info-municipios',
        api_views.InfoMunicipiosAPIView.as_view(),
        name='municipios_info_api'
    ),
]
