from django.urls import path
from Usuario import views

# Asumiendo que tendrás vistas para CRUD de Trabajador en el futuro
# from .views import TrabajadorDetailView, ...

urlpatterns = [
    path('register/', views.trabajador_register, name='trabajador-register'),
    #path('<int:pk>/', TrabajadorDetailView.as_view(), name='trabajador-detail'),
    path('employee/', views.employeeView, name='employee-view'),
]