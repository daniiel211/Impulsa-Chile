import requests
from django.conf import settings
import json

def buscar_ofertas_jooble(keywords="desarrollador", location="Chile", page=1):
    """
    Busca ofertas en la API de Jooble para Chile.
    Documentación: https://cl.jooble.org/api/about
    """
    # Endpoint de Jooble (requiere API Key en la URL o Header)
    # La key debe estar en settings.JOOBLE_API_KEY
    api_key = getattr(settings, 'JOOBLE_API_KEY', '')
    if api_key:
        api_key = str(api_key).strip().strip("'").strip('"')
    
    endpoint = f"https://cl.jooble.org/api/{api_key}"
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Jooble usa POST para las búsquedas
    payload = {
        "keywords": keywords,
        "location": location,
        "page": page,
        "resultonpage": 10
    }

    # Log to file for debugging
    try:
        with open("debug_jooble.log", "a") as f:
            f.write(f"--- New Request ---\n")
            f.write(f"API Key: {api_key}\n")
            f.write(f"Endpoint: {endpoint}\n")
            f.write(f"Payload: {payload}\n")
    except Exception:
        pass

    try:
        print(f"DEBUG: Consultando Jooble API. Endpoint: {endpoint}")
        
        if not api_key:
            print("ERROR: No se ha configurado JOOBLE_API_KEY en settings.")
            try:
                with open("debug_jooble.log", "a") as f:
                    f.write("ERROR: Missing API Key\n")
            except Exception:
                pass
            return []

        response = requests.post(endpoint, json=payload, headers=headers)
        
        try:
            with open("debug_jooble.log", "a") as f:
                f.write(f"Status Code: {response.status_code}\n")
                f.write(f"Response: {response.text[:500]}\n")
        except Exception:
            pass

        print(f"DEBUG: Status Code: {response.status_code}")
        
        response.raise_for_status()
        data = response.json()
        
        # Jooble devuelve { "totalCount": 123, "jobs": [...] }
        jobs = data.get('jobs', [])
        
        # Normalizamos los datos para que el template no falle
        # El template espera: title, redirect_url, company.display_name, location.display_name, description, created
        results = []
        for job in jobs:
            results.append({
                'title': job.get('title'),
                'redirect_url': job.get('link'),
                'company': {'display_name': job.get('company', 'Confidencial')},
                'location': {'display_name': job.get('location')},
                'description': job.get('snippet', ''),
                'created': job.get('updated', '')
            })
            
        print(f"DEBUG: Resultados encontrados: {len(results)}")
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Error conectando con Jooble: {e}")
        if 'response' in locals():
             print(f"DEBUG: Response content: {response.text}")
        try:
            with open("debug_jooble.log", "a") as f:
                f.write(f"Exception: {e}\n")
        except Exception:
            pass
        return []