"""ROM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import RedirectView
from common.views import LoginUsuario
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from common.views import InitialView, user_logout, RegisterView

urlpatterns = [
    path('credicol-register/', RegisterView.as_view(), name='register'),
    path('admin/', admin.site.urls),
    path('dashboard/', InitialView.as_view(), name='initial_view'),
    path('', RedirectView.as_view(url='/login/')),
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('transacciones/', include('transacciones.urls')),
    path('common/', include('common.urls')),
    path('clientes/', include('clientes.urls')),
    path('productos/', include('productos.urls')),
    path('gastos/', include('gastos.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
