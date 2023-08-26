FROM python:3.9
WORKDIR /routes
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src /routes/src
ENV ENV_FILE .env.development
EXPOSE 3002
CMD FLASK_APP=./src/main.py flask run -h 0.0.0.0 -p 3002