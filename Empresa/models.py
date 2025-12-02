from django.db import models
from django.contrib.auth.models import User

class Industria(models.Model):
    nombre_industria = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre_industria

class Empresa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    industria = models.ForeignKey(Industria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Industria")
    rut = models.CharField("RUT", max_length=12, unique=True, help_text="RUT de la empresa sin puntos y con guión.")
    razon_social = models.CharField("Razón Social", max_length=255)
    descripcion = models.TextField("Descripción", blank=True)
    ubicacion_texto = models.CharField("Ubicación", max_length=255, blank=True, help_text="Ej: Santiago, RM")
    tamano_rango = models.CharField("Tamaño", max_length=50, blank=True, help_text="Ej: 51–200 personas")
    por_que_elegirla = models.TextField("Por qué elegirla", blank=True, help_text="Una razón por línea.")
    roles_clave = models.TextField("Roles clave", blank=True, help_text="Separados por coma, ej: Full-Stack Developer, Data Analyst")

    def __str__(self):
        return self.razon_social

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
