from django.urls import path
from .views import (
    EmpresaListView,
    EmpresaDetailView,
    EmpresaCreateView,
    EmpresaUpdateView,
    EmpresaDeleteView,
)

urlpatterns = [
    path('', EmpresaListView.as_view(), name='empresa-list'),
    path('nueva/', EmpresaCreateView.as_view(), name='empresa-create'),
    path('<int:pk>/', EmpresaDetailView.as_view(), name='empresa-detail'),
    path('<int:pk>/editar/', EmpresaUpdateView.as_view(), name='empresa-update'),
    path('<int:pk>/eliminar/', EmpresaDeleteView.as_view(), name='empresa-delete'),
]
