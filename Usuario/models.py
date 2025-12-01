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

class Certificacion(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, related_name='certificaciones')
    nombre = models.CharField(max_length=200, blank=True)
    archivo = models.FileField(upload_to='certificaciones/', blank=False, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        base = self.nombre or "Certificación"
        return f"{base} de {self.trabajador.usuario.username}"

class Employee (models. Model) :
    id = models. IntegerField(primary_key=True)
    name = models. CharField(max_length=50)
    email = models. CharField(max_length=50)
    salary = models. DecimalField(max_digits=10, decimal_places=2)

    def __str__ (self) :
        return str(self.id) + " " + self.name + "($" + str(self.salary) + ")"