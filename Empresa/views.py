from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from .models import Empresa
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

FEATURED_SUGGESTIONS = [
    {
        'slug': 'technova-spa',
        'nombre': 'TechNova SpA',
        'industria': 'Tecnología',
        'resumen': 'Plataformas SaaS para PYMEs, con foco en automatización y análisis.',
        'ubicacion': 'Santiago, RM',
        'tamano': '51–200',
        'por_que_elegirla': [
            'Cultura de aprendizaje continuo y certificaciones internas.',
            'Stack moderno (Python, Django, React, AWS).',
            'Planes de carrera claros y mentorías.',
        ],
        'roles_clave': ['Full-Stack Developer', 'Data Analyst', 'Customer Success']
    },
    {
        'slug': 'agroverde-ltda',
        'nombre': 'AgroVerde Ltda.',
        'industria': 'Agroindustria',
        'resumen': 'Soluciones de trazabilidad y eficiencia para productores agrícolas.',
        'ubicacion': 'Curicó, Maule',
        'tamano': '11–50',
        'por_que_elegirla': [
            'Impacto directo en sostenibilidad y productividad.',
            'Equipos pequeños, alta autonomía.',
            'Proyectos en campo y tecnologías IoT.',
        ],
        'roles_clave': ['IoT Technician', 'Field Operations', 'Data Engineer']
    },
    {
        'slug': 'finclarity-sa',
        'nombre': 'FinClarity S.A.',
        'industria': 'Servicios financieros',
        'resumen': 'Productos digitales para inclusión financiera y educación económica.',
        'ubicacion': 'Las Condes, RM',
        'tamano': '201–500',
        'por_que_elegirla': [
            'Propósito social y proyectos con alto alcance.',
            'Capacitación formal y certificaciones exigidas.',
            'Beneficios flexibles y bienestar.',
        ],
        'roles_clave': ['Product Manager', 'QA Automation', 'UX Researcher']
    },
    {
        'slug': 'educonnect',
        'nombre': 'EduConnect',
        'industria': 'EdTech',
        'resumen': 'Plataformas de aprendizaje y empleabilidad con enfoque LATAM.',
        'ubicacion': 'Remoto (Chile)',
        'tamano': '51–200',
        'por_que_elegirla': [
            'Impacto en formación y empleabilidad.',
            'Trabajo 100% remoto y horarios flexibles.',
            'Stack moderno y buenas prácticas.',
        ],
        'roles_clave': ['Frontend Developer', 'Content Specialist', 'SEO Analyst']
    },
]

class EmpresaListView(ListView):
    model = Empresa
    template_name = 'empresa/empresa_list.html'
    context_object_name = 'empresas'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(razon_social__icontains=q) | Q(descripcion__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sugerencias'] = FEATURED_SUGGESTIONS
        return context


class FeaturedEmpresaDetailView(TemplateView):
    template_name = 'empresa/empresa_destacada_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        match = next((e for e in FEATURED_SUGGESTIONS if e['slug'] == slug), None)
        if not match:
            raise Http404('Empresa destacada no encontrada')
        context['e'] = match
        return context

class EmpresaDetailView(DetailView):
    model = Empresa
    template_name = 'empresa/empresa_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        e = self.object
        razones = []
        roles = []
        if e.por_que_elegirla:
            razones = [r.strip() for r in e.por_que_elegirla.splitlines() if r.strip()]
        if e.roles_clave:
            roles = [r.strip() for r in e.roles_clave.split(',') if r.strip()]
        ctx['razones_list'] = razones
        ctx['roles_list'] = roles
        return ctx

class EmpresaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Empresa
    fields = ['industria', 'rut', 'razon_social', 'descripcion', 'ubicacion_texto', 'tamano_rango', 'por_que_elegirla', 'roles_clave']
    template_name = 'empresa/empresa_form.html'
    success_url = reverse_lazy('empresa-list')
    permission_required = 'Empresa.add_empresa'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class EmpresaUpdateView(UpdateView):
    model = Empresa
    fields = ['industria', 'rut', 'razon_social', 'descripcion', 'ubicacion_texto', 'tamano_rango', 'por_que_elegirla', 'roles_clave']
    template_name = 'empresa/empresa_form.html'
    success_url = reverse_lazy('empresa-list')

class EmpresaDeleteView(DeleteView):
    model = Empresa
    template_name = 'empresa/empresa_confirm_delete.html'
    success_url = reverse_lazy('empresa-list')
