from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.trabajador_register, name='trabajador-register'),
    path('login/', auth_views.LoginView.as_view(template_name='Usuario/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # You can add other auth URLs here if needed (password reset, etc.)
]