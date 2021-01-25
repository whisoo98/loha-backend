# pull official base image
FROM python:3.8.6-alpine as builder

RUN apk update && apk add bash
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# module for postgresql
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install clayful
RUN pip install psycopg2
RUN pip install iamporter
RUN apk add tk
#RUN pip install -U install channels==2.2
RUN pip install channels_redis

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
