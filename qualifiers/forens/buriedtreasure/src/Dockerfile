FROM alpine:latest

RUN apk add --no-cache mktorrent transmission-cli

WORKDIR /data
COPY absolute_cinema.zip .
COPY absolute_cinema.torrent .

EXPOSE 51413/tcp 51413/udp

ENTRYPOINT ["transmission-cli", "-w", "/data", "absolute_cinema.torrent"]