from django.urls import path

from . import views, api_views

app_name = 'productos'
urlpatterns = [
    path('', views.ListProductosView.as_view(), name='productos_list'),
    path(
        'api/productos/<str:producto_id>',
        api_views.ListarProductosAPIView.as_view(),
        name='listar_productos_api'
    ),
    # path('cliente/<int:id>', views.ClienteDetailView.as_view(), name='profile'),
    path('add-new', views.AddProductoView.as_view(), name='add_new_producto'),
    path('editar-producto/<int:pk>', views.EditarProductoView.as_view(), name='editar_producto'),
    path('detalle/<int:pk>', views.DetailProductoView.as_view(), name='detalle_producto'),
    # path('editar-cliente/<int:pk>', views.ClienteEditView.as_view(), name='edit_cliente'),
]
