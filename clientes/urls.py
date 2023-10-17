from django.urls import path

from . import views, api_views

app_name = 'clientes'
urlpatterns = [
    path('', views.ListUsersView.as_view(), name='clientes_list'),
    path('api/clientes/', api_views.ListarClientesAPIView.as_view(), name='listar_clientes_api'),
    path('cliente/<int:id>', views.ClienteDetailView.as_view(), name='profile'),
    path('add-new', views.AddClienteView.as_view(), name='add_new_cliente'),
    path('editar-cliente/<int:pk>', views.ClienteEditView.as_view(), name='edit_cliente'),
]
