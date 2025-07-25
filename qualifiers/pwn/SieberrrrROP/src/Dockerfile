# Dockerfile for SieberrrrROP challenge
FROM ubuntu AS app

FROM pwn.red/jail
COPY --from=app / /srv

COPY ./vuln /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
RUN chmod +x /srv/app/run

ENV JAIL_TIME=60
