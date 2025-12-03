from django.contrib import admin
from .models import OfertaEmpleo, Region, Tipo_Contrato

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('nombre_region',)

@admin.register(Tipo_Contrato)
class TipoContratoAdmin(admin.ModelAdmin):
    list_display = ('nombre_contrato',)

@admin.register(OfertaEmpleo)
class OfertaEmpleoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'region', 'estado', 'fecha_publicacion', 'es_externa')
    list_filter = ('estado', 'region', 'tipo_contrato', 'es_externa')
    search_fields = ('titulo', 'descripcion', 'empresa__razon_social')
