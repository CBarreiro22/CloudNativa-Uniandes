FROM python:3.10-alpine
WORKDIR /users
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src /users/src
ENV ENV_FILE .env.development
EXPOSE 3015
CMD FLASK_APP=./src/main.py flask run -h 0.0.0.0 -p 3015