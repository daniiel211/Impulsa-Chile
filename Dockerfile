# Recomendación: Usa 3.11 o 3.12 si 3.13 te da problemas de compatibilidad con librerías.
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y fuerza salida en consola en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema (necesarias para mysqlclient y otros)
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . /app/

# NOTA: No necesitamos CMD aquí porque railway.json lo sobrescribe.
# Pero dejamos este por si quieres probarlo localmente con Docker.
CMD gunicorn EvES2.wsgi:application --bind 0.0.0.0:$PORT