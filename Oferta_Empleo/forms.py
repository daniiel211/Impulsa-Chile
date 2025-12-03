from django import forms
from .models import OfertaEmpleo

class OfertaEmpleoForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Ofertas de Empleo.
    El campo 'empresa' se excluye porque se asignará automáticamente
    desde el usuario que ha iniciado sesión.
    """
    class Meta:
        model = OfertaEmpleo
        fields = [
            'titulo', 'descripcion', 'region', 'tipo_contrato', 
            'estado', 'direccion_texto', 'latitud', 'longitud',
            'id_externo_adzuna', 'url_postulacion_externa', 'es_externa'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 5}),
            'latitud': forms.HiddenInput(), # Ocultamos lat/lon si se obtienen con un mapa
            'longitud': forms.HiddenInput(),
        }