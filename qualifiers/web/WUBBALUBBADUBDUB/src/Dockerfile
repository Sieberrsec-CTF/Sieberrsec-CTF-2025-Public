FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY PickleRick.py .
COPY templates/ templates/
COPY flag.txt .

RUN chmod 444 flag.txt
RUN mkdir uploads
RUN chmod 777 uploads

CMD flask run --host=0.0.0.0 --port 1234
