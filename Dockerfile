#Arranco de un contenedor (como una PC virtual) que ya tiene python instalado
FROM python:3.9-slim

#Dentro de ese contenedor creo una carpeta llamada 'app', puede ser cualquier cosa
WORKDIR /app

# Copio el proyecto que tengo en mi mac (el primer .) a la nueva carpeta app del contenedor (el segundo .)
COPY . .

# En el contenedor, instalo las dependencias
RUN pip install -r requirements.txt

# Corro el programa EN EL CONTENEDOR
CMD ["python", "main.py"]