from django.shortcuts import render
from Empresa.models import Empresa
from Oferta_Empleo.models import OfertaEmpleo


def inicio(request):
    es_empresa = False
    empresa_obj = None
    empresa_stats = {}
    if request.user.is_authenticated:
        try:
            empresa_obj = Empresa.objects.get(usuario=request.user)
            es_empresa = True
        except Empresa.DoesNotExist:
            es_empresa = False
        if es_empresa:
            qs = OfertaEmpleo.objects.filter(empresa=empresa_obj)
            empresa_stats = {
                'total': qs.count(),
                'abiertas': qs.filter(estado='AB').count(),
                'cerradas': qs.filter(estado='CE').count(),
                'pausadas': qs.filter(estado='PA').count(),
            }
    return render(request, 'inicio.html', {
        'es_empresa': es_empresa,
        'empresa_obj': empresa_obj,
        'empresa_ofertas_stats': empresa_stats,
    })
