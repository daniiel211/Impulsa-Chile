from django.urls import path
from .views import (
    EmpresaListView,
    EmpresaDetailView,
    EmpresaCreateView,
    EmpresaUpdateView,
    EmpresaDeleteView,
    FeaturedEmpresaDetailView,
    empresa_dashboard_view,
)

urlpatterns = [
    path('', EmpresaListView.as_view(), name='empresa-list'),
    path('dashboard/', empresa_dashboard_view, name='empresa-dashboard'),
    path('nueva/', EmpresaCreateView.as_view(), name='empresa-create'),
    path('<int:pk>/', EmpresaDetailView.as_view(), name='empresa-detail'),
    path('<int:pk>/editar/', EmpresaUpdateView.as_view(), name='empresa-update'),
    path('<int:pk>/eliminar/', EmpresaDeleteView.as_view(), name='empresa-delete'),
    path('destacada/<slug:slug>/', FeaturedEmpresaDetailView.as_view(), name='empresa-destacada'),
]
