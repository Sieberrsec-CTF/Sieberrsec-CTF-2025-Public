FROM ubuntu AS app

FROM pwn.red/jail
COPY --from=app / /srv

COPY ./photoshop /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
COPY ./icon.png /srv/app/icon.png
RUN chmod +x /srv/app/run

ENV JAIL_TIME=60 