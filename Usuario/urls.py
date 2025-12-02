from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_choice, name='register-choice'),
    path('register/trabajador/', views.trabajador_register, name='trabajador-register'),
    path('register/empresa/', views.empresa_register, name='empresa-register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    # Añadimos el `next_page` aquí para asegurar la redirección.
    path('logout/', views.CustomLogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('perfil/habilidades/agregar/', views.add_habilidades, name='usuario-add-habilidades'),
    path('perfil/actualizar/', views.profile_update, name='usuario-profile-update'),
    path('perfil/resumen/', views.perfil_resumen, name='usuario-perfil-resumen'),
    # You can add other auth URLs here if needed (password reset, etc.)
]
