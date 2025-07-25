# Dockerfile sample if you are running a binary
# feel free to specify a version e.g. ubuntu:22.04
FROM ubuntu AS app

FROM pwn.red/jail
COPY --from=app / /srv

COPY ./headquarters2 /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
RUN chmod +x /srv/app/run

ENV JAIL_TIME=60 

# Dockerfile sample if you are running a python script
# FROM python:slim AS app

# FROM pwn.red/jail
# COPY --from=app / /srv

# COPY ./{{python_file_name}}.py /srv/app/run
# COPY ./flag.txt /srv/app/flag.txt
# RUN chmod +x /srv/app/run

# ENV JAIL_TIME=60
