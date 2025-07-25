FROM python:3.12-alpine AS app
COPY requirements.txt .
RUN pip install -r requirements.txt


FROM pwn.red/jail
COPY --from=app / /srv

COPY h2math.py /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod +x /srv/app/run

ENV JAIL_TIME=60
ENV JAIL_MEM=0
ENV JAIL_CPU=0