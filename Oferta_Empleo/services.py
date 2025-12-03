import requests
import requests
from django.conf import settings
from .models import OfertaEmpleo, Region, Tipo_Contrato
from Empresa.models import Empresa
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

def sincronizar_ofertas_jooble(query="desarrollador", location="Chile"):
    API_KEY = getattr(settings, 'JOOBLE_API_KEY', '')
    
    if not API_KEY:
        print("Faltan credenciales de Jooble")
        return

    url = f"https://jooble.org/api/{API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "keywords": query,
        "location": location,
        "resultonpage": 10
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        resultados = data.get('jobs', [])

        # Asegurar región y tipo de contrato por defecto
        region_default, _ = Region.objects.get_or_create(nombre_region="Externa")
        tipo_contrato_default, _ = Tipo_Contrato.objects.get_or_create(nombre_contrato="No especificado")

        for item in resultados:
            jooble_id = str(item.get('id'))
            
            # 1. Gestionar la Empresa (Evitar duplicados)
            nombre_empresa = item.get('company', 'Empresa Confidencial')
            
            # Buscamos la empresa por razón social, si no existe, la creamos
            try:
                empresa_obj = Empresa.objects.get(razon_social=nombre_empresa)
            except Empresa.DoesNotExist:
                # Crear usuario dummy
                username = f"jooble_{get_random_string(8)}"
                user = User.objects.create_user(username=username, email=f"{username}@example.com", password=get_random_string(16))
                
                empresa_obj = Empresa.objects.create(
                    usuario=user,
                    razon_social=nombre_empresa,
                    rut=f"EXT-{get_random_string(8)}", # RUT ficticio
                    descripcion='Empresa importada desde Jooble',
                    ubicacion_texto=item.get('location', ''),
                )

            # 2. Guardar o Actualizar la Oferta
            # Nota: Jooble no siempre devuelve un ID único estable, pero usamos 'id' si existe.
            if jooble_id:
                oferta, created = OfertaEmpleo.objects.update_or_create(
                    id_externo_adzuna=jooble_id, # Reutilizamos este campo para el ID externo
                    defaults={
                        'titulo': item.get('title'),
                        'descripcion': item.get('snippet', ''),
                        'empresa': empresa_obj,
                        'region': region_default,
                        'direccion_texto': item.get('location', ''),
                        'tipo_contrato': tipo_contrato_default,
                        'url_postulacion_externa': item.get('link'),
                        'es_externa': True,
                        'fecha_publicacion': item.get('updated'),
                        'estado': OfertaEmpleo.EstadoOferta.ABIERTA,
                    }
                )
            
    except Exception as e:
        print(f"Error sincronizando Jooble: {e}")