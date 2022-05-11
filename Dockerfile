FROM python:3.7-bullseye
RUN apt update && apt -y upgrade
RUN apt -y install gnupg software-properties-common curl
RUN curl -fsSL https://apt.releases.hashicorp.com/gpg > key
RUN apt-key add ./key
RUN apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com bullseye main"
RUN echo deb http://ppa.launchpad.net/ansible/ansible/ubuntu focal main >> /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
RUN apt update && apt -y install terraform ansible


COPY ./ app/

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

ENV FLASK_APP=/app/vmlab.py

EXPOSE 5000

ENTRYPOINT [ "./boot.sh" ]
