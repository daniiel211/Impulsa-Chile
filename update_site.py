import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EvES2.settings')
django.setup()

from django.contrib.sites.models import Site

def update_site():
    try:
        site = Site.objects.get(pk=1)
        site.domain = '127.0.0.1:8000'
        site.name = 'Impulsa Chile Local'
        site.save()
        print(f"Successfully updated Site ID 1 to: {site.domain}")
    except Site.DoesNotExist:
        print("Site ID 1 does not exist. Creating it...")
        Site.objects.create(pk=1, domain='127.0.0.1:8000', name='Impulsa Chile Local')
        print("Created Site ID 1: 127.0.0.1:8000")

if __name__ == '__main__':
    update_site()
