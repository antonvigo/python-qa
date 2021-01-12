FROM python:3.7.3-slim-stretch
MAINTAINER Ilia Ilin "ii@rebrainme.com"

RUN apt-get update && apt-get install -y python3-pip

WORKDIR /webapp

ADD requirements.txt /webapp

COPY . /webapp

RUN pip3 install uwsgi
RUN pip3 install -r requirements.txt

ENV HOME /webapp
WORKDIR /webapp

EXPOSE 8000
ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8000", "--module", "calc2:APP", "--processes", "1", "--threads", "1"]
