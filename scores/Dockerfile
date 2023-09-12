FROM python:3.10-alpine
WORKDIR /scores
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src /scores/src
ENV ENV_FILE .env.development
EXPOSE 3004
CMD FLASK_APP=./src/main.py flask run -h 0.0.0.0 -p 3004