from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Empresa

class EmpresaListView(ListView):
    model = Empresa
    template_name = 'Empresa/empresa_list.html'
    context_object_name = 'empresas'

class EmpresaDetailView(DetailView):
    model = Empresa
    template_name = 'Empresa/empresa_detail.html'

class EmpresaCreateView(CreateView):
    model = Empresa
    fields = ['usuario', 'industria', 'rut', 'razon_social', 'descripcion']
    template_name = 'Empresa/empresa_form.html'
    success_url = reverse_lazy('empresa-list')

class EmpresaUpdateView(UpdateView):
    model = Empresa
    fields = ['industria', 'rut', 'razon_social', 'descripcion']
    template_name = 'Empresa/empresa_form.html'
    success_url = reverse_lazy('empresa-list')

class EmpresaDeleteView(DeleteView):
    model = Empresa
    template_name = 'Empresa/empresa_confirm_delete.html'
    success_url = reverse_lazy('empresa-list')