FROM ubuntu:18.04

RUN apt update && apt install -y build-essential

WORKDIR /src

CMD /bin/bash