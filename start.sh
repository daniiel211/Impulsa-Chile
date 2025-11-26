#!/bin/bash

# --- 1. Ejecutar Migraciones (opcional, pero recomendado) ---
# Esto aplica cualquier cambio pendiente en la base de datos.
echo "Aplicando migraciones de la base de datos..."
python manage.py migrate
echo "Migraciones aplicadas."

# --- 2. Recolectar Archivos Estáticos (opcional) ---
# Esto copia todos los archivos estáticos (CSS, JS, imágenes) a un solo directorio 
# para que el servidor web pueda servirlos eficientemente.
# Asegúrate de que STATIC_ROOT esté configurado en settings.py
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput
echo "Archivos estáticos recolectados."

# --- 3. Iniciar el Servidor WSGI (Gunicorn) ---
# Reemplaza 'nombre_del_proyecto' con el nombre de tu directorio de proyecto 
# que contiene settings.py y wsgi.py. 
# Basado en tu estructura de archivos, parece ser 'EvES2'.
# Ajusta el número de workers (-w) y el socket/puerto (-b).

# Formato: gunicorn [OPCIONES] [MODULO_WSGI]:[APLICACION]
echo "Iniciando Gunicorn..."
exec gunicorn EvES2.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    --log-level info