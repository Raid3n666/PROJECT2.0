FROM python:slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD gunicorn\ --bind\ 0.0.0.0:\$PORT\ app:app