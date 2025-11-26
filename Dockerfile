# Utiliza una imagen base de Python apropiada (ajusta la versión 3.13)
FROM python:3.13-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias de sistema necesarias para mysqlclient
# 'default-libmysqlclient-dev' contiene los headers y libs para compilar.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Copia el archivo de requisitos e instala las dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu código
COPY . /app/

# Define el comando de inicio para Gunicorn (asumiendo que tu app se llama EvES2)
ENV PORT 8000
CMD gunicorn EvES2.wsgi:application --bind 0.0.0.0:$PORT