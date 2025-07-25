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
RUN echo $'<?xml version="1.0" encoding="UTF-8"?>\n\
<oor:items xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n\
<item oor:path="/org.openoffice.Office.Calc/Content/Update"><prop oor:name="Link" oor:op="fuse"><value>0</value></prop></item>\n\
<item oor:path="/org.openoffice.Office.Common/Security/Scripting"><prop oor:name="SecureURL" oor:op="fuse"><value><it>$(home)</it></value></prop></item>\n\
</oor:items>' > ~/.config/libreoffice/4/user/registrymodifications.xcu

RUN libreoffice --headless submissions/submissions.csv

RUN mv Module1.xba ~/.config/libreoffice/4/user/basic/Standard/Module1.xba

RUN pip3 install -r requirements.txt

CMD ["python3", "-u", "-m", "gunicorn", "--bind", "0.0.0.0", "app:app", "--workers", "5"]

EXPOSE 8000
