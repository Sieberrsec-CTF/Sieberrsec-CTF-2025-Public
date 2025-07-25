from ubuntu:20.04@sha256:8feb4d8ca5354def3d8fce243717141ce31e2c428701f6682bd2fafe15388214

run apt update && apt install -y software-properties-common && \
  add-apt-repository ppa:deadsnakes/ppa && \
  apt update && \
  apt install -y python3.9 python3-pip socat && \
  python3.9 -m pip install RestrictedPython

copy ./chall/ /app/
copy ./mutuple.cpython-39-x86_64-linux-gnu.so /usr/local/lib/python3.9/dist-packages

workdir /app
run chmod 744 ./flag.txt
run chmod +x ./server.py ./run.py

run useradd -ms /bin/bash jail
user jail
env PYTHONUNBUFFERED=y

cmd socat tcp4-listen:5000,fork,reuseaddr exec:/app/server.py
