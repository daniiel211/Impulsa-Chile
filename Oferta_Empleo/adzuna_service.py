import requests
from django.conf import settings

def buscar_ofertas_adzuna(query="desarrollador", location="chile", page=1):
    """
    Busca ofertas en la API de Adzuna para Chile.
    """
    # URL base para Chile (cl)
    endpoint = f"https://api.adzuna.com/v1/api/jobs/cl/search/{page}"
    
    params = {
        'app_id': settings.ADZUNA_APP_ID,
        'app_key': settings.ADZUNA_APP_KEY,
        'what': query,        # Término de búsqueda (ej. Python, Vendedor)
        'where': location,    # Ubicación (ej. Santiago, Concepción)
        'content-type': 'application/json',
        'results_per_page': 10
    }

    try:
        print(f"DEBUG: Consultando Adzuna API. Endpoint: {endpoint}")
        print(f"DEBUG: Params: app_id={params['app_id']}, app_key={params['app_key']}, what={params['what']}, where={params['where']}")
        
        response = requests.get(endpoint, params=params)
        print(f"DEBUG: Status Code: {response.status_code}")
        
        response.raise_for_status() # Lanza error si la petición falla (404, 500)
        data = response.json()
        
        results = data.get('results', [])
        print(f"DEBUG: Resultados encontrados: {len(results)}")
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Error conectando con Adzuna: {e}")
        if 'response' in locals():
             print(f"DEBUG: Response content: {response.text}")
        return []