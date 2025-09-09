# Imagen base
FROM python:3.13-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar herramientas de compilación y dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    build-essential \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /kavak/app

# Copiar requirements
COPY requirements.txt .

# Actualizar pip e instalar dependencias
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Descargar modelo de SpaCy
RUN python -m spacy download es_core_news_sm

# Copiar el resto de la app
COPY app ./app

# Exponer puerto de la API
EXPOSE 8000

# Comando para iniciar la API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
