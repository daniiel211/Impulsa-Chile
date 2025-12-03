import requests
from django.conf import settings
from .models import OfertaEmpleo, Region, Tipo_Contrato
from Empresa.models import Empresa
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

def sincronizar_ofertas_adzuna(query="desarrollador", location="chile"):
    APP_ID = settings.ADZUNA_APP_ID
    APP_KEY = settings.ADZUNA_APP_KEY
    
    if not APP_ID or not APP_KEY:
        print("Faltan credenciales de Adzuna")
        return

    url = f"https://api.adzuna.com/v1/api/jobs/cl/search/1"
    params = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'what': query,
        'where': location,
        'results_per_page': 10,
        'content-type': 'application/json',
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        resultados = data.get('results', [])

        # Asegurar región y tipo de contrato por defecto
        region_default, _ = Region.objects.get_or_create(nombre_region="Externa")
        tipo_contrato_default, _ = Tipo_Contrato.objects.get_or_create(nombre_contrato="No especificado")

        for item in resultados:
            adzuna_id = str(item.get('id'))
            
            # 1. Gestionar la Empresa (Evitar duplicados)
            nombre_empresa = item.get('company', {}).get('display_name', 'Empresa Confidencial')
            
            # Buscamos la empresa por razón social, si no existe, la creamos
            # Nota: Empresa tiene OneToOne con User. Necesitamos un usuario dummy para empresas externas.
            try:
                empresa_obj = Empresa.objects.get(razon_social=nombre_empresa)
            except Empresa.DoesNotExist:
                # Crear usuario dummy
                username = f"adzuna_{get_random_string(8)}"
                user = User.objects.create_user(username=username, email=f"{username}@example.com", password=get_random_string(16))
                
                empresa_obj = Empresa.objects.create(
                    usuario=user,
                    razon_social=nombre_empresa,
                    rut=f"EXT-{get_random_string(8)}", # RUT ficticio
                    descripcion='Empresa importada desde Adzuna',
                    ubicacion_texto=item.get('location', {}).get('display_name', ''),
                )

            # 2. Guardar o Actualizar la Oferta
            oferta, created = OfertaEmpleo.objects.update_or_create(
                id_externo_adzuna=adzuna_id,
                defaults={
                    'titulo': item.get('title'),
                    'descripcion': item.get('description'),
                    'empresa': empresa_obj,
                    'region': region_default, # Usamos región por defecto o mapeamos si es posible
                    'direccion_texto': item.get('location', {}).get('display_name'),
                    'tipo_contrato': tipo_contrato_default,
                    'url_postulacion_externa': item.get('redirect_url'),
                    'es_externa': True,
                    'fecha_publicacion': item.get('created'),
                    'estado': OfertaEmpleo.EstadoOferta.ABIERTA,
                }
            )
            
    except Exception as e:
        print(f"Error sincronizando Adzuna: {e}")