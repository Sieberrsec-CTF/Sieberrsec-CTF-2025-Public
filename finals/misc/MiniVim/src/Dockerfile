FROM python:slim AS app

FROM pwn.red/jail
COPY --from=app / /srv

COPY ./jail.py /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
RUN chmod +x /srv/app/run

ENV JAIL_TIME=60
ENV JAIL_MEM=0
ENV JAIL_CPU=0
ENV TERM=xterm-256color 
