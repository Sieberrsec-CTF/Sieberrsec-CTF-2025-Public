# Dockerfile sample if you are running a binary
# feel free to specify a version e.g. ubuntu:22.04
FROM ubuntu AS app

FROM pwn.red/jail
COPY --from=app / /srv

COPY ./game /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
RUN chmod +x /srv/app/run

ENV JAIL_MEM=0
ENV JAIL_CPU=0
ENV JAIL_TIME=3600 