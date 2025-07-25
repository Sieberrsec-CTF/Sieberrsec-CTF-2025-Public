FROM python:3.12-alpine AS app

FROM pwn.red/jail
COPY --from=app / /srv

COPY ./jail.py /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
COPY ./chiyo.txt /srv/app/chiyo.txt
RUN chmod +x /srv/app/run

ENV JAIL_MEM=0
ENV JAIL_CPU=0
ENV JAIL_TIME=60