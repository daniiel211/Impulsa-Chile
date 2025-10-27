from django.urls import path
from .views import (
    OfertaEmpleoListView,
    OfertaEmpleoDetailView,
    OfertaEmpleoCreateView,
    OfertaEmpleoUpdateView,
    OfertaEmpleoDeleteView,
)

urlpatterns = [
    path('', OfertaEmpleoListView.as_view(), name='ofertaempleo-list'),
    path('nueva/', OfertaEmpleoCreateView.as_view(), name='ofertaempleo-create'),
    path('<int:pk>/', OfertaEmpleoDetailView.as_view(), name='ofertaempleo-detail'),
    path('<int:pk>/editar/', OfertaEmpleoUpdateView.as_view(), name='ofertaempleo-update'),
    path('<int:pk>/eliminar/', OfertaEmpleoDeleteView.as_view(), name='ofertaempleo-delete'),
]