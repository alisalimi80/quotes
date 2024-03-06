FROM python:3.9-buster

WORKDIR /master/

ENV PYTHONPATH /master/
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt

RUN rm -f "/etc/localtime" &&\
    ln -s /usr/share/zoneinfo/Asia/Tehran /etc/localtime &&\
    apt-get update &&\
    apt-get install -y build-essential libpq-dev ncat netcat

RUN pip install --upgrade pip

RUN pip install -r /requirements.txt


COPY . .