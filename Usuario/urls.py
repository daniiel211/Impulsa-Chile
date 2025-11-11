from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('register/', views.trabajador_register, name='trabajador-register'),
    path('login/', auth_views.LoginView.as_view(template_name='Usuario/login.html'), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('habilidades/add/', views.add_habilidades, name='usuario-add-habilidades'),
    path('profile/update/', views.profile_update, name='usuario-profile-update'),
    path('perfil/resumen/', views.perfil_resumen, name='usuario-perfil-resumen'),
    # You can add other auth URLs here if needed (password reset, etc.)
]