from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.trabajador_register, name='trabajador-register'),
    path('login/', auth_views.LoginView.as_view(template_name='Usuario/login.html'), name='login'),
    # Añadimos el `next_page` aquí para asegurar la redirección.
    path('logout/', views.CustomLogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('perfil/habilidades/agregar/', views.add_habilidades, name='usuario-add-habilidades'),
    path('perfil/actualizar/', views.profile_update, name='usuario-profile-update'),
    path('perfil/resumen/', views.perfil_resumen, name='usuario-perfil-resumen'),
    # You can add other auth URLs here if needed (password reset, etc.)
]