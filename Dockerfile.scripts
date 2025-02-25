FROM python:3.9.15-alpine

RUN apk update && apk add --no-cache bash

WORKDIR /home

COPY ./requirements.txt .

RUN pip install -r requirements.txt