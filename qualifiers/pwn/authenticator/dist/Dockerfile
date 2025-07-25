FROM ubuntu:25.04 AS app

FROM pwn.red/jail
COPY --from=app / /srv

COPY ./authenticator /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
RUN chmod +x /srv/app/run

ENV JAIL_TIME=600