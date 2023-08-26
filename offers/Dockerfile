# Utilizamos la imagen base de Python 3.10
FROM python:3.10

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /offers

# Copiamos el archivo requirements.txt a la imagen
COPY requirements.txt .

# Instalamos las dependencias del proyecto
RUN pip install -r requirements.txt

# Copiamos la carpeta src al directorio de trabajo en la imagen
COPY src /offers/src

# Exponemos el puerto 3000
EXPOSE 3003

# Definimos una variable de entorno para el archivo .env.development
ENV ENV_FILE .env.development

# Comando para correr la aplicación Flask
CMD FLASK_APP=./src/main.py flask run -h 0.0.0.0 -p 3003