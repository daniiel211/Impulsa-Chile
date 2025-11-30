#!/bin/bash

# --- SEGURIDAD: Definir puerto por defecto si Railway falla ---
# Si PORT no existe, usa 8000. Si existe, usa el de Railway.
PORT=${PORT:-8000}

echo "1. Aplicando migraciones..."
python manage.py migrate

echo "2. Recolectando estáticos..."
python manage.py collectstatic --noinput

echo "3. Iniciando Gunicorn en puerto $PORT..."
# OJO: Usamos comillas DOBLES " " para que lea la variable, y todo en una línea.
exec gunicorn EvES2.wsgi:application --bind "0.0.0.0:$PORT" --workers 4 --log-level info