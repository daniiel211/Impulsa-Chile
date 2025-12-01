from django.urls import reverse_lazy
from django.shortcuts import render
from django.db.models import Q
from .services import buscar_licitaciones
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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

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
    template_name = 'Empresa/empresa_list.html'
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
    template_name = 'Empresa/empresa_destacada_detail.html'

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
    template_name = 'Empresa/empresa_detail.html'

class EmpresaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Empresa
    fields = ['industria', 'rut', 'razon_social', 'descripcion']
    template_name = 'Empresa/empresa_form.html'
    success_url = reverse_lazy('empresa-list')
    permission_required = 'Empresa.add_empresa'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class EmpresaUpdateView(UpdateView):
    model = Empresa
    fields = ['industria', 'rut', 'razon_social', 'descripcion']
    template_name = 'Empresa/empresa_form.html'
    success_url = reverse_lazy('empresa-list')

class EmpresaDeleteView(DeleteView):
    model = Empresa
    template_name = 'Empresa/empresa_confirm_delete.html'
    success_url = reverse_lazy('empresa-list')


def buscador_oportunidades(request):
    oportunidades = []
    query = request.GET.get('q', '') # Lo que el usuario escribe en el buscador
    
    if query:
        # Llamamos a nuestro servicio
        oportunidades = buscar_licitaciones(filtro_palabra_clave=query)
    
    return render(request, 'oportunidades.html', {
        'oportunidades': oportunidades,
        'query': query
    })

@login_required
def empresa_dashboard_view(request):
    """
    Dashboard para el usuario de tipo Empresa.
    Muestra estadísticas y accesos directos relevantes para su propia empresa.
    """
    try:
        # 1. Obtenemos la empresa asociada al usuario logueado
        empresa = Empresa.objects.get(usuario=request.user)
    except Empresa.DoesNotExist:
        # Si el usuario no tiene una empresa, no puede ver este dashboard.
        # Podrías redirigirlo o mostrar un error. Http404 es una opción segura.
        raise Http404("No tienes una empresa asociada a tu cuenta.")

    # 2. Filtramos las ofertas de empleo que pertenecen a ESTA empresa
    ofertas_de_la_empresa = empresa.ofertaempleo_set.all()

    # 3. Calculamos estadísticas específicas
    total_ofertas = ofertas_de_la_empresa.count()
    ofertas_abiertas = ofertas_de_la_empresa.filter(estado='AB').count()
    ofertas_cerradas = ofertas_de_la_empresa.filter(estado='CE').count()

    # 4. Obtenemos las últimas 5 ofertas publicadas por la empresa
    ofertas_recientes = ofertas_de_la_empresa.order_by('-fecha_publicacion')[:5]

    context = {
        'empresa': empresa,
        'total_ofertas': total_ofertas,
        'ofertas_abiertas': ofertas_abiertas,
        'ofertas_cerradas': ofertas_cerradas,
        'ofertas_recientes': ofertas_recientes,
    }
    return render(request, 'Empresa/empresa_dashboard.html', context)