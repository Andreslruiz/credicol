from django.urls import path

from . import api_views
from . import views

app_name = 'gastos'

urlpatterns = [
    path(
        '',
        views.ListAllGastosView.as_view(),
        name='full_gastos_list'
    ),
    path(
        'api/gastos/',
        api_views.ListarAllGastosAPIView.as_view(),
        name='listar_all_gastos_api'
    ),
    path('add-gasto/', views.AddGastoView.as_view(), name='add_gasto'),
    path(
        'edit-gasto/<int:pk>/', views.EditGastoView.as_view(),
        name='edit_gasto'
    ),
]
