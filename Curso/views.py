from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Curso
from Usuario.models import Trabajador

class CursoListView(ListView):
    model = Curso
    template_name = 'curso/curso_list.html'
    context_object_name = 'cursos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            perfil = Trabajador.objects.filter(usuario=user).first()
            context['trabajador'] = perfil
            context['user_habilidades'] = perfil.habilidades.all() if perfil else []
        return context

class CursoDetailView(DetailView):
    model = Curso
    template_name = 'curso/curso_detail.html'

class CursoCreateView(LoginRequiredMixin, CreateView):
    model = Curso
    fields = ['titulo', 'descripcion', 'duracion_horas', 'url_contenido']
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('curso-list')

class CursoUpdateView(LoginRequiredMixin, UpdateView):
    model = Curso
    fields = ['titulo', 'descripcion', 'duracion_horas', 'url_contenido']
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('curso-list')

class CursoDeleteView(LoginRequiredMixin, DeleteView):
    model = Curso
    template_name = 'curso/curso_confirm_delete.html'
    success_url = reverse_lazy('curso-list')