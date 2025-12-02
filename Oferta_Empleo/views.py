from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import OfertaEmpleo, Region, Tipo_Contrato
from Empresa.models import Empresa
from django.conf import settings
from django.core.serializers import serialize
import json
from django.shortcuts import render
from django.db.models import Count

INDUSTRY_TEMPLATES = {
    'Tecnología': [
        {
            'title': 'Desarrollador/a Backend Python',
            'desc': """Responsabilidades: construir APIs y microservicios.
Requisitos: Python, Django/DRF.
Beneficios: remoto, capacitación."""
        },
        {
            'title': 'DevOps Engineer',
            'desc': """Responsabilidades: CI/CD y infraestructura.
Requisitos: Docker, Kubernetes, AWS.
Beneficios: certificaciones, bono."""
        },
    ],
    'Retail': [
        {
            'title': 'Jefe/a de Tienda',
            'desc': """Responsabilidades: operación y equipo.
Requisitos: liderazgo, indicadores.
Beneficios: comisiones, capacitación."""
        },
        {
            'title': 'Analista de Inventario',
            'desc': """Responsabilidades: control y reportes.
Requisitos: Excel avanzado, ERP.
Beneficios: horario flexible."""
        },
    ],
    'Salud': [
        {
            'title': 'TENS',
            'desc': """Responsabilidades: apoyo clínico.
Requisitos: título, experiencia.
Beneficios: turnos, colación."""
        },
        {
            'title': 'Recepcionista Clínica',
            'desc': """Responsabilidades: atención y agenda.
Requisitos: trato, sistemas.
Beneficios: desarrollo, beneficios."""
        },
    ],
    'Educación': [
        {
            'title': 'Docente Matemáticas',
            'desc': """Responsabilidades: clases y evaluación.
Requisitos: título, didáctica.
Beneficios: capacitación."""
        },
        {
            'title': 'Coordinador/a Académico',
            'desc': """Responsabilidades: planificación y seguimiento.
Requisitos: gestión educativa.
Beneficios: estabilidad."""
        },
    ],
    'default': [],
}

class OfertaEmpleoListView(ListView):
    model = OfertaEmpleo
    template_name = 'oferta_empleo/ofertaempleo_list.html'
    context_object_name = 'ofertas'

    def get_queryset(self):
        qs = super().get_queryset()
        empresa_id = self.request.GET.get('empresa_id')
        if empresa_id:
            qs = qs.filter(empresa__pk=empresa_id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

class OfertaEmpleoDetailView(DetailView):
    model = OfertaEmpleo
    template_name = 'oferta_empleo/ofertaempleo_detail.html'

class OfertaEmpleoCreateView(LoginRequiredMixin, CreateView):
    model = OfertaEmpleo
    fields = ['region', 'tipo_contrato', 'titulo', 'descripcion', 'estado']
    template_name = 'oferta_empleo/ofertaempleo_form.html'
    success_url = reverse_lazy('ofertaempleo-list')

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            from .models import Region, Tipo_Contrato
            for nombre in [
                    'Arica y Parinacota',
                    'Tarapacá',
                    'Antofagasta',
                    'Atacama',
                    'Coquimbo',
                    'Valparaíso',
                    'Metropolitana de Santiago',
                    "O'Higgins",
                    'Maule',
                    'Ñuble',
                    'Biobío',
                    'La Araucanía',
                    'Los Ríos',
                    'Los Lagos',
                    'Aysén',
                    'Magallanes y Antártica Chilena',
            ]:
                Region.objects.get_or_create(nombre_region=nombre)
            if not Tipo_Contrato.objects.exists():
                for nombre in ['Tiempo completo', 'Medio tiempo', 'Temporal', 'Práctica']:
                    Tipo_Contrato.objects.get_or_create(nombre_contrato=nombre)
            first_region = Region.objects.order_by('id').first()
            initial['estado'] = 'AB'
            if first_region:
                initial['region'] = first_region.pk
        return initial

    def get(self, request, *args, **kwargs):
        from .models import Region, Tipo_Contrato
        for nombre in [
                'Arica y Parinacota',
                'Tarapacá',
                'Antofagasta',
                'Atacama',
                'Coquimbo',
                'Valparaíso',
                'Metropolitana de Santiago',
                "O'Higgins",
                'Maule',
                'Ñuble',
                'Biobío',
                'La Araucanía',
                'Los Ríos',
                'Los Lagos',
                'Aysén',
                'Magallanes y Antártica Chilena',
        ]:
            Region.objects.get_or_create(nombre_region=nombre)
        if not Tipo_Contrato.objects.exists():
            for nombre in ['Tiempo completo', 'Medio tiempo', 'Temporal', 'Práctica']:
                Tipo_Contrato.objects.get_or_create(nombre_contrato=nombre)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        industry_name = None
        examples = INDUSTRY_TEMPLATES['default']
        try:
            empresa = Empresa.objects.get(usuario=self.request.user)
            if empresa.industria and empresa.industria.nombre_industria:
                industry_name = empresa.industria.nombre_industria
                examples = INDUSTRY_TEMPLATES.get(industry_name, examples)
        except Empresa.DoesNotExist:
            pass
        ctx['industry_name'] = industry_name
        ctx['industry_examples'] = examples
        return ctx

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        from django.forms import TextInput, NumberInput, EmailInput, Textarea, Select
        for name, field in form.fields.items():
            widget = field.widget
            if isinstance(widget, (TextInput, NumberInput, EmailInput)):
                widget.attrs.update({'class': 'form-control'})
            elif isinstance(widget, Textarea):
                widget.attrs.update({'class': 'form-control', 'rows': 6})
            elif isinstance(widget, Select):
                widget.attrs.update({'class': 'form-select'})
        if 'titulo' in form.fields:
            form.fields['titulo'].widget.attrs.update({'placeholder': 'Desarrollador/a Full-Stack (Python/Django)'})
        if 'descripcion' in form.fields:
            form.fields['descripcion'].widget.attrs.update({'placeholder': 'Responsabilidades: desarrollar features y mantener aplicaciones web.\nRequisitos: 2+ años de experiencia, Python/Django, front-end básico.\nOfrecemos: modalidad híbrida, seguro complementario, plan de capacitación.'})
        return form

    def get_success_url(self):
        try:
            empresa = Empresa.objects.get(usuario=self.request.user)
            return reverse_lazy('ofertaempleo-list') + f'?empresa_id={empresa.pk}'
        except Empresa.DoesNotExist:
            return super().get_success_url()

    def form_valid(self, form):
        from Empresa.models import Empresa
        try:
            empresa = Empresa.objects.get(usuario=self.request.user)
        except Empresa.DoesNotExist:
            form.add_error(None, 'Debes registrar tu empresa para publicar ofertas.')
            return self.form_invalid(form)
        form.instance.empresa = empresa
        return super().form_valid(form)

class OfertaEmpleoUpdateView(LoginRequiredMixin, UpdateView):
    model = OfertaEmpleo
    fields = ['empresa', 'region', 'tipo_contrato', 'titulo', 'descripcion', 'estado']
    template_name = 'oferta_empleo/ofertaempleo_form.html'
    success_url = reverse_lazy('ofertaempleo-list')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(empresa__usuario=self.request.user)

class OfertaEmpleoDeleteView(LoginRequiredMixin, DeleteView):
    model = OfertaEmpleo
    template_name = 'oferta_empleo/ofertaempleo_confirm_delete.html'
    success_url = reverse_lazy('ofertaempleo-list')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(empresa__usuario=self.request.user)

def mapa_ofertas_view(request):
    # Obtener todas las ofertas que tienen coordenadas válidas
    ofertas = OfertaEmpleo.objects.exclude(latitud__isnull=True).exclude(longitud__isnull=True)
    
    # Serializar los datos para pasarlos a JSON de forma segura
    ofertas_json = serialize('json', ofertas, fields=('pk', 'titulo', 'latitud', 'longitud', 'direccion_texto'))

    context = {
        'mapbox_access_token': settings.MAPBOX_ACCESS_TOKEN,
        'ofertas_json': ofertas_json,
    }
    return render(request, 'oferta_empleo/mapa_ofertas.html', context)

def dashboard_ofertas_view(request):
    # 1. Estadísticas clave
    total_ofertas = OfertaEmpleo.objects.count()
    ofertas_abiertas = OfertaEmpleo.objects.filter(estado='AB').count()
    ofertas_cerradas = OfertaEmpleo.objects.filter(estado='CE').count()
    ofertas_pausadas = OfertaEmpleo.objects.filter(estado='PA').count()

    # 2. Datos para gráficos
    # Ofertas por región
    ofertas_por_region = (
        OfertaEmpleo.objects.values('region__nombre_region')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # Ofertas por tipo de contrato
    ofertas_por_contrato = (
        OfertaEmpleo.objects.values('tipo_contrato__nombre_contrato')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # 3. Actividad reciente
    ofertas_recientes = OfertaEmpleo.objects.order_by('-fecha_publicacion')[:5]

    context = {
        'total_ofertas': total_ofertas,
        'ofertas_abiertas': ofertas_abiertas,
        'ofertas_cerradas': ofertas_cerradas,
        'ofertas_pausadas': ofertas_pausadas,
        'ofertas_por_region_json': json.dumps(list(ofertas_por_region)),
        'ofertas_por_contrato_json': json.dumps(list(ofertas_por_contrato)),
        'ofertas_recientes': ofertas_recientes,
    }

    return render(request, 'Oferta_Empleo/dashboard_ofertas.html', context)
