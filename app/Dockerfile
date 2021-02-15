# pull official base image
FROM python:3.8.6

# set work directory
WORKDIR /usr/src/app

# vim 설치
RUN apt-get -y update
RUN apt-get -y upgrade

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install clayful
RUN pip install psycopg2
RUN pip install iamporter
RUN pip install -U channels
RUN pip install channels_redis
RUN pip install -U Daphne
# redis
# pip install pypiwin32

COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install django_extensions
# copy project
COPY . .
