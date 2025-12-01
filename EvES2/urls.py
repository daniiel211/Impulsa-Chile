"""
URL configuration for EvES2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import include, reverse_lazy
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirige la ruta raíz a la página de login
    path('', RedirectView.as_view(url=reverse_lazy('login')), name='root-redirect-to-login'),
    path('inicio/', views.inicio, name='Inicio'), # Página de inicio, ahora con el nombre 'Inicio'
    path('cursos/', include('Curso.urls')),
    path('empresas/', include('Empresa.urls')),
    path('accounts/', include('allauth.urls')), # URLs para autenticación (login, logout, social)
    path('usuarios/', include('Usuario.urls')), # This now correctly points to your new urls.py
    path('ofertas/', include('Oferta_Empleo.urls')),
]
