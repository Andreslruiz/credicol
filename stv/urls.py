from django.urls import path
from . import views
from . import api_views

app_name = 'stv'

urlpatterns = [
    path('', views.InitialStvView.as_view(), name='initial_stv'),
    path('login', views.LoginStvUser.as_view(), name='stv_login'),
    path('reports', views.ListReportsView.as_view(), name='report_list'),
    path(
        'api/stv-reportes/',
        api_views.ListarReportesAPIView.as_view(),
        name='listar_reportes_api'
    ),
    path('add-new-report', views.AddReportView.as_view(), name='add_new_report'),
    path('download-report/<int:id>', views.download_report, name='download_report'),
]
