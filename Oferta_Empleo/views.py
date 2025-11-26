from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import OfertaEmpleo
from Empresa.models import Empresa

class OfertaEmpleoListView(ListView):
    model = OfertaEmpleo
    template_name = 'oferta_empleo/ofertaempleo_list.html'
    context_object_name = 'ofertas'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

class OfertaEmpleoDetailView(DetailView):
    model = OfertaEmpleo
    template_name = 'oferta_empleo/ofertaempleo_detail.html'

class OfertaEmpleoCreateView(LoginRequiredMixin, CreateView):
    model = OfertaEmpleo
    fields = ['empresa', 'region', 'tipo_contrato', 'titulo', 'descripcion', 'estado']
    template_name = 'oferta_empleo/ofertaempleo_form.html'
    success_url = reverse_lazy('ofertaempleo-list')

class OfertaEmpleoUpdateView(LoginRequiredMixin, UpdateView):
    model = OfertaEmpleo
    fields = ['empresa', 'region', 'tipo_contrato', 'titulo', 'descripcion', 'estado']
    template_name = 'oferta_empleo/ofertaempleo_form.html'
    success_url = reverse_lazy('ofertaempleo-list')

class OfertaEmpleoDeleteView(LoginRequiredMixin, DeleteView):
    model = OfertaEmpleo
    template_name = 'oferta_empleo/ofertaempleo_confirm_delete.html'
    success_url = reverse_lazy('ofertaempleo-list')