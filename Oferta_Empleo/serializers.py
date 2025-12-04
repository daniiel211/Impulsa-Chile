from rest_framework import serializers
from .models import OfertaEmpleo, Region, Tipo_Contrato
from Empresa.models import Empresa

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class TipoContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Contrato
        fields = '__all__'

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['usuario', 'razon_social', 'rut', 'ubicacion_texto', 'descripcion']

class OfertaEmpleoSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    tipo_contrato = TipoContratoSerializer(read_only=True)
    empresa = EmpresaSerializer(read_only=True)
    
    # Para escrituras, podríamos necesitar PrimaryKeyRelatedField si queremos permitir crear ofertas via API
    # Pero para "API interna" de consulta, nested serializers son mejores.
    # Si se requiere escritura, se pueden añadir campos _id adicionales.
    
    class Meta:
        model = OfertaEmpleo
        fields = '__all__'
        read_only_fields = ('empresa',)
