from django.urls import path

from . import views, api_views

app_name = 'clientes'
urlpatterns = [
    path('', views.ListUsersView.as_view(), name='clientes_list'),
    path('api/clientes/', api_views.ListarClientesAPIView.as_view(), name='listar_clientes_api'),
    path('cliente/<int:id>', views.ClienteDetailView.as_view(), name='profile')
]
