from django.db import models
from django.contrib.auth.models import User 

class Habilidad(models.Model):
    nombre_habilidad = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre_habilidad

class Trabajador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    resumen_profesional = models.TextField("Resumen Profesional", blank=True, null=True)
    cv = models.FileField("Currículum (PDF)", upload_to='cvs/', blank=True, null=True)
    habilidades = models.ManyToManyField(Habilidad, blank=True)

    def __str__(self):
        return self.usuario.username

    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"