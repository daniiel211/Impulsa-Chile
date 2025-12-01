from django.db import models
from Empresa.models import Empresa 

class Region(models.Model):
    nombre_region = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre_region

class Tipo_Contrato(models.Model):
    nombre_contrato = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre_contrato

    class Meta:
        verbose_name = "Tipo de Contrato"
        verbose_name_plural = "Tipos de Contrato"

class OfertaEmpleo(models.Model):
    class EstadoOferta(models.TextChoices):
        ABIERTA = 'AB', 'Abierta'
        CERRADA = 'CE', 'Cerrada'
        PAUSADA = 'PA', 'Pausada'
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa")
    region = models.ForeignKey(Region, on_delete=models.PROTECT, verbose_name="Región")
    tipo_contrato = models.ForeignKey(
        Tipo_Contrato, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Tipo de Contrato"
    )
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    direccion_texto = models.CharField(max_length=255, blank=True, null=True)
    titulo = models.CharField("Título de la Oferta", max_length=255)
    descripcion = models.TextField("Descripción del Puesto")
    estado = models.CharField(
        max_length=2,
        choices=EstadoOferta.choices,
        default=EstadoOferta.ABIERTA,
        verbose_name="Estado"
    )
    fecha_publicacion = models.DateTimeField("Fecha de Publicación", auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.empresa.razon_social}"

    class Meta:
        verbose_name = "Oferta de Empleo"
        verbose_name_plural = "Ofertas de Empleo"
        ordering = ['-fecha_publicacion']