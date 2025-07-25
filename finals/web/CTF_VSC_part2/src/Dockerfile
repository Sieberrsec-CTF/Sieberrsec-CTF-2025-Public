FROM python:3.10-slim

COPY . .
RUN useradd -ms /bin/bash ctf
COPY . /home/ctf
RUN chown ctf /home/ctf/*
WORKDIR /home/ctf

RUN apt-get update
RUN apt install --no-install-recommends -y libreoffice-calc default-jre libreoffice-java-common

USER ctf

RUN mkdir -p ~/.config/libreoffice/4/user

RUN libreoffice --headless submissions/submissions.csv

RUN mv Module1.xba ~/.config/libreoffice/4/user/basic/Standard/Module1.xba

RUN pip3 install -r requirements.txt

CMD ["python3", "-u", "-m", "gunicorn", "--bind", "0.0.0.0", "app:app", "--workers", "5"]

EXPOSE 8000
