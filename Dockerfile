FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ ./src/

# Crear directorio para logs
RUN mkdir -p /app/logs

# Agregar src al PYTHONPATH
ENV PYTHONPATH=/app/src

# Exponer puerto
EXPOSE 5001

# Comando por defecto
CMD ["python", "-m", "content_management.main"]
