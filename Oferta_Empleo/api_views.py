from rest_framework import viewsets
from .models import OfertaEmpleo, Region, Tipo_Contrato
from .serializers import OfertaEmpleoSerializer, RegionSerializer, TipoContratoSerializer

class OfertaEmpleoViewSet(viewsets.ModelViewSet):
    queryset = OfertaEmpleo.objects.all().order_by('-fecha_publicacion')
    serializer_class = OfertaEmpleoSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Opcional: configurar permisos

    def perform_create(self, serializer):
        # Asignamos automáticamente la empresa del usuario logueado
        # Asume que el usuario tiene una empresa asociada (user.empresa)
        serializer.save(empresa=self.request.user.empresa)

class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class TipoContratoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tipo_Contrato.objects.all()
    serializer_class = TipoContratoSerializer
