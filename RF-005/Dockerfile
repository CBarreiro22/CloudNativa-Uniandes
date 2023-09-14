FROM python:3.10-alpine
WORKDIR /RF-005
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src /RF-005/src
ENV ENV_FILE .env.development
EXPOSE 3005
CMD FLASK_APP=./src/main.py flask run -h 0.0.0.0 -p 3005