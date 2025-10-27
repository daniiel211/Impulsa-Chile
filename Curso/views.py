from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Curso

class CursoListView(ListView):
    model = Curso
    template_name = 'curso/curso_list.html'
    context_object_name = 'cursos'

class CursoDetailView(DetailView):
    model = Curso
    template_name = 'curso/curso_detail.html'

class CursoCreateView(CreateView):
    model = Curso
    fields = ['titulo', 'descripcion', 'duracion_horas', 'url_contenido']
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('curso-list')

class CursoUpdateView(UpdateView):
    model = Curso
    fields = ['titulo', 'descripcion', 'duracion_horas', 'url_contenido']
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('curso-list')

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'curso/curso_confirm_delete.html'
    success_url = reverse_lazy('curso-list')