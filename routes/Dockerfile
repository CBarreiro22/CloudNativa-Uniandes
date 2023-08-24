FROM python:3.9.12
WORKDIR /routes
COPY requirements.txt .

RUN pip install -r requirements.txt

#RUN pipenv install   

# Cambiar de directorio de trabajo a donde esta el ejectuable del API
#WORKDIR /app

# Instalar requerimientos de la app
#RUN pip install -r requirements.txt

# Copiar el contenido del directorio actual en la imagen de docker

COPY src /routes/src

ENV VERSION=1.0
ENV DB_USER=routesu
ENV DB_PASSWORD=routesp
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_NAME=routesdb
ENV USERS_PATH=3000

EXPOSE 3002
# Archivo principal donde corre el API
CMD FLASK_APP=./src/main.py flask run -h 0.0.0.0 -p 3002