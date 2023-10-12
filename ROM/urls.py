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

from common.views import InitialView, user_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', InitialView.as_view(), name='initial_view'),
    path('', RedirectView.as_view(url='/login/')),
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('ventas/', include('ventas.urls')),
    path('common/', include('common.urls')),
]
