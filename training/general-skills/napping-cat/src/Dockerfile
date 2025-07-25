FROM ubuntu AS app

FROM pwn.red/jail
COPY --from=app / /srv

COPY ./napping-cat /srv/app/run
RUN chmod +x /srv/app/run

ENV JAIL_TIME=60 

