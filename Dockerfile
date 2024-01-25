FROM python:3.9 as base
ENV PYTHONUNBUFFERED 1

ARG SECRET_KEY

WORKDIR /usr/src/core-api

RUN apt-get update && apt-get install -y gettext

COPY . /usr/src/core-api
COPY ./requirements.txt /usr/src/core-api
RUN pip install -r requirements.txt
COPY ./entrypoint.sh /usr/src/core-api

RUN chmod +x ./entrypoint.sh

EXPOSE 8000
