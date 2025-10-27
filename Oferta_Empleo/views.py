from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import OfertaEmpleo

class OfertaEmpleoListView(ListView):
    model = OfertaEmpleo
    template_name = 'oferta_empleo/ofertaempleo_list.html'
    context_object_name = 'ofertas'

class OfertaEmpleoDetailView(DetailView):
    model = OfertaEmpleo
    template_name = 'oferta_empleo/ofertaempleo_detail.html'

class OfertaEmpleoCreateView(CreateView):
    model = OfertaEmpleo
    fields = ['empresa', 'region', 'tipo_contrato', 'titulo', 'descripcion', 'estado']
    template_name = 'oferta_empleo/ofertaempleo_form.html'
    success_url = reverse_lazy('ofertaempleo-list')

class OfertaEmpleoUpdateView(UpdateView):
    model = OfertaEmpleo
    fields = ['empresa', 'region', 'tipo_contrato', 'titulo', 'descripcion', 'estado']
    template_name = 'oferta_empleo/ofertaempleo_form.html'
    success_url = reverse_lazy('ofertaempleo-list')

class OfertaEmpleoDeleteView(DeleteView):
    model = OfertaEmpleo
    template_name = 'oferta_empleo/ofertaempleo_confirm_delete.html'
    success_url = reverse_lazy('ofertaempleo-list')