from django.urls import path
from .views import (
    OfertaEmpleoListView,
    OfertaEmpleoDetailView,
    OfertaEmpleoCreateView,
    OfertaEmpleoUpdateView,
    OfertaEmpleoDeleteView,
    mapa_ofertas_view,
    dashboard_ofertas_view,
    buscar_empleos,
)

urlpatterns = [
    # Rutas para vistas generales y de creación
    path('', OfertaEmpleoListView.as_view(), name='ofertaempleo-list'),
    path('nueva/', OfertaEmpleoCreateView.as_view(), name='ofertaempleo-create'),
    path('dashboard/', dashboard_ofertas_view, name='ofertaempleo-dashboard'),
    path('mapa/', mapa_ofertas_view, name='ofertaempleo-mapa'),
    path('buscar/', buscar_empleos, name='ofertaempleo-buscar'),
    # Rutas para una oferta de empleo específica (detalle, edición, eliminación)
    path('<int:pk>/', OfertaEmpleoDetailView.as_view(), name='ofertaempleo-detail'),
    path('<int:pk>/editar/', OfertaEmpleoUpdateView.as_view(), name='ofertaempleo-update'),
    path('<int:pk>/eliminar/', OfertaEmpleoDeleteView.as_view(), name='ofertaempleo-delete'),
]