FROM python:3.10-alpine
WORKDIR /RF-006
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src /RF-006/src
EXPOSE 3012
ENV ENV_FILE .env.development
CMD FLASK_APP=./src/main.py flask run -h 0.0.0.0 -p 3012