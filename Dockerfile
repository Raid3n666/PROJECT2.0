FROM python:slim

WORKDIR /app

COPY app.py .
COPY templates /app/
COPY static /app/
COPY modules /app/
COPY db /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python app.py