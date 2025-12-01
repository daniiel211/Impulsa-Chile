from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import OfertaEmpleo, Region, Tipo_Contrato
from Empresa.models import Empresa
from .forms import OfertaEmpleoForm
from django.conf import settings
from django.core.serializers import serialize
import json
from django.shortcuts import render
from django.db.models import Count

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

class EmpresaRequiredMixin(UserPassesTestMixin):
    """Asegura que el usuario logueado tenga una empresa asociada."""
    def test_func(self):
        return hasattr(self.request.user, 'empresa')

    def handle_no_permission(self):
        # Opcional: podrías redirigir a una página para crear una empresa
        # con un mensaje de advertencia.
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("No tienes una empresa asociada para realizar esta acción.")

class OfertaEmpleoCreateView(LoginRequiredMixin, EmpresaRequiredMixin, CreateView):
    model = OfertaEmpleo
    form_class = OfertaEmpleoForm
    template_name = 'oferta_empleo/ofertaempleo_form.html'
    success_url = reverse_lazy('empresa-dashboard') # Redirige al dashboard de la empresa

    def form_valid(self, form):
        # Asigna la empresa del usuario actual a la oferta de empleo
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_access_token'] = settings.MAPBOX_ACCESS_TOKEN
        return context

class OfertaEmpleoUpdateView(LoginRequiredMixin, EmpresaRequiredMixin, UpdateView):
    model = OfertaEmpleo
    form_class = OfertaEmpleoForm
    template_name = 'oferta_empleo/ofertaempleo_form.html'
    success_url = reverse_lazy('empresa-dashboard')

    def get_queryset(self):
        # Asegura que un usuario solo pueda editar ofertas de su propia empresa
        queryset = super().get_queryset()
        return queryset.filter(empresa=self.request.user.empresa)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_access_token'] = settings.MAPBOX_ACCESS_TOKEN
        return context

class OfertaEmpleoDeleteView(LoginRequiredMixin, EmpresaRequiredMixin, DeleteView):
    model = OfertaEmpleo
    template_name = 'oferta_empleo/ofertaempleo_confirm_delete.html'
    success_url = reverse_lazy('ofertaempleo-list')

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
    query = request.GET.get('q', '')

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
    ofertas_recientes = OfertaEmpleo.objects.order_by('-fecha_publicacion')
    if query:
        ofertas_recientes = ofertas_recientes.filter(titulo__icontains=query)
    else:
        ofertas_recientes = ofertas_recientes[:10] # Mostramos 10 si no hay búsqueda

    context = {
        'total_ofertas': total_ofertas,
        'ofertas_abiertas': ofertas_abiertas,
        'query': query,
        'ofertas_cerradas': ofertas_cerradas,
        'ofertas_pausadas': ofertas_pausadas,
        'ofertas_por_region_json': json.dumps(list(ofertas_por_region)),
        'ofertas_por_contrato_json': json.dumps(list(ofertas_por_contrato)),
        'ofertas_recientes': ofertas_recientes,
    }

    return render(request, 'oferta_empleo/dashboard_ofertas.html', context)