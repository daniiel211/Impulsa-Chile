from django.urls import path
from .views import (
    OfertaEmpleoListView,
    OfertaEmpleoDetailView,
    OfertaEmpleoCreateView,
    OfertaEmpleoUpdateView,
    OfertaEmpleoDeleteView,
    mapa_ofertas_view,
    dashboard_ofertas_view,
)

urlpatterns = [
    # Rutas para vistas generales y de creación
    path('ofertas/', OfertaEmpleoListView.as_view(), name='ofertaempleo-list'),
    path('ofertas/nueva/', OfertaEmpleoCreateView.as_view(), name='ofertaempleo-create'),
    path('ofertas/dashboard/', dashboard_ofertas_view, name='ofertaempleo-dashboard'),
    path('ofertas/mapa/', mapa_ofertas_view, name='ofertaempleo-mapa'),
    # Rutas para una oferta de empleo específica (detalle, edición, eliminación)
    path('ofertas/<int:pk>/', OfertaEmpleoDetailView.as_view(), name='ofertaempleo-detail'),
    path('ofertas/<int:pk>/editar/', OfertaEmpleoUpdateView.as_view(), name='ofertaempleo-update'),
    path('ofertas/<int:pk>/eliminar/', OfertaEmpleoDeleteView.as_view(), name='ofertaempleo-delete'),
]