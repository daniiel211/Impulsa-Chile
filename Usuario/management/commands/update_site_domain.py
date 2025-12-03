from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
import os

class Command(BaseCommand):
    help = 'Actualiza el dominio del sitio para Google Auth en producción'

    def handle(self, *args, **kwargs):
        domain = os.getenv('RAILWAY_PUBLIC_DOMAIN')
        if not domain:
            self.stdout.write(self.style.WARNING('RAILWAY_PUBLIC_DOMAIN no está configurada. Usando valor por defecto o ignorando.'))
            return

        # Asegurarse de que no tenga protocolo
        domain = domain.replace('https://', '').replace('http://', '')
        
        try:
            site = Site.objects.get(pk=1)
            site.domain = domain
            site.name = 'Impulsa Chile'
            site.save()
            self.stdout.write(self.style.SUCCESS(f'Sitio actualizado exitosamente a: {domain}'))
        except Site.DoesNotExist:
            Site.objects.create(pk=1, domain=domain, name='Impulsa Chile')
            self.stdout.write(self.style.SUCCESS(f'Sitio creado exitosamente: {domain}'))
