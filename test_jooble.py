import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv('JOOBLE_API_KEY')
print(f"API KEY: {API_KEY}")

def test_endpoint(base_url):
    endpoint = f"{base_url}/{API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "keywords": "Vendedor",
        "location": "Santiago",
        "page": 1,
        "resultonpage": 10
    }

    print(f"\nTesting Endpoint: {endpoint}")
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                jobs = data.get('jobs', [])
                print(f"Jobs found: {len(jobs)}")
            except Exception as e:
                print(f"JSON Decode Error: {e}")
                print(f"Response start: {response.text[:200]}")
        else:
            print(f"Request failed. Response start: {response.text[:200]}")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    if not API_KEY:
        print("NO API KEY")
    else:
        test_endpoint("https://jooble.org/api")
        test_endpoint("https://cl.jooble.org/api")
