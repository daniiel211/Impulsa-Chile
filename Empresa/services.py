import requests
import datetime
import logging
from django.conf import settings
from django.core.cache import cache

# Configuramos un logger para ver errores en la consola de Django
logger = logging.getLogger(__name__)

# Constantes
API_URL = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
CACHE_TIMEOUT = 7200  # 2 horas en segundos

def _consultar_api_mercado_publico():
    """
    Función interna que consulta la API o recupera los datos de la caché.
    Retorna la lista cruda de licitaciones del día.
    """
    # 1. Generamos la fecha de hoy formato ddmmaaaa (Ej: 01122025)
    fecha_hoy = datetime.datetime.now().strftime("%d%m%Y")
    cache_key = f"mercadopublico_licitaciones_{fecha_hoy}"

    # 2. Intentamos obtener datos de la memoria caché
    datos_cacheados = cache.get(cache_key)
    if datos_cacheados:
        logger.info(f"Recuperando licitaciones desde CACHÉ ({len(datos_cacheados)} items)")
        return datos_cacheados

    # 3. Si no hay caché, consultamos la API Externa
    params = {
        'fecha': fecha_hoy,
        'estado': 'activas', # Solo traemos las que se pueden postular
        'ticket': settings.MERCADO_PUBLICO_TICKET
    }

    try:
        logger.info("Consultando API externa Mercado Público...")
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status() # Lanza error si el status no es 200 OK
        
        data = response.json()
        
        # La API devuelve un objeto con metadata, la lista está en 'Listado'
        lista_licitaciones = data.get('Listado', [])
        
        # 4. Guardamos en caché si la lista no está vacía
        if lista_licitaciones:
            cache.set(cache_key, lista_licitaciones, CACHE_TIMEOUT)
            logger.info("Datos guardados en caché exitosamente.")
            
        return lista_licitaciones

    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión con Mercado Público: {e}")
        return []
    except ValueError as e:
        logger.error(f"Error decodificando JSON: {e}")
        return []

def buscar_licitaciones(filtro_palabra_clave=None):
    """
    Función pública para usar en tus views.py.
    Filtra las licitaciones por palabra clave y formatea los datos para el template.
    """
    # Obtenemos la lista completa (desde caché o API)
    lista_completa = _consultar_api_mercado_publico()
    
    resultados = []
    
    # Si no hay lista (error de API o día feriado sin datos), retornamos vacío
    if not lista_completa:
        return []

    # Si no hay filtro, retornamos todo (Opcional: podrías limitar a las primeras 20)
    if not filtro_palabra_clave:
        return _formatear_datos(lista_completa[:20]) # Limitamos a 20 para no saturar

    palabra = filtro_palabra_clave.lower()
    
    # Filtramos en Python
    for item in lista_completa:
        # Usamos .get('', '') para evitar errores si falta un campo
        nombre = item.get('Nombre', '').lower()
        descripcion = item.get('Descripcion', '').lower()
        rubro = item.get('Rubro', '').lower()

        if palabra in nombre or palabra in descripcion or palabra in rubro:
            resultados.append(item)

    return _formatear_datos(resultados)

def _formatear_datos(lista_cruda):
    """
    Limpia los datos para que sean fáciles de usar en el HTML.
    Crea el link directo a la licitación.
    """
    datos_limpios = []
    for item in lista_cruda:
        codigo = item.get('CodigoExterno')
        datos_limpios.append({
            'codigo': codigo,
            'nombre': item.get('Nombre'),
            'cierre': item.get('FechaCierre'), # Viene como string fecha
            'moneda': item.get('Moneda'),
            'monto_estimado': item.get('MontoEstimado', 'No especificado'),
            # Construimos el link directo para que la Pyme vaya a postular
            'link_postulacion': f"http://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs={codigo}"
        })
    return datos_limpios