# FROM python:3.10-slim-bullseye

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     xinetd python3 python3-pip && \
#     rm -rf /var/lib/apt/lists/*

# RUN pip3 install --no-cache-dir pycryptodome

# RUN mkdir -m 777 /app
# WORKDIR /app

# COPY . /app/
# COPY vivi.xinetd /etc/xinetd.d/vivi

# RUN chmod +x /app/chall.py

# EXPOSE 20001

# CMD ["xinetd", "-dontfork"]
FROM python:slim AS app
RUN pip install --no-cache-dir pycryptodome

FROM pwn.red/jail
COPY --from=app / /srv

COPY ./chall.py /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
RUN chmod +x /srv/app/run

ENV JAIL_TIME=60
ENV JAIL_MEM=0
ENV JAIL_CPU=0
