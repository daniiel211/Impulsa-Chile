from django.db import models

class Curso(models.Model):
    titulo = models.CharField("Título del Curso", max_length=255)
    descripcion = models.TextField("Descripción", blank=True)
    duracion_horas = models.PositiveIntegerField(
        "Duración en Horas", 
        null=True, 
        blank=True,
        help_text="Duración total estimada del curso en horas."
    )
    url_contenido = models.URLField(
        "Enlace al Contenido", 
        max_length=2083, 
        blank=True,
        help_text="URL externa donde se aloja el material del curso."
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['titulo']