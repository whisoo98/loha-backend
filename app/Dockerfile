# pull official base image
FROM python:3.8.6

# set work directory
WORKDIR /usr/src/app

# vim 설치
RUN apt-get update && apt-get install -y gettext python3-dev libpq-dev

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install clayful
RUN pip install psycopg2
RUN pip install iamport-rest-client
RUN pip install -U channels
RUN pip install channels_redis
RUN pip install firebase-admin
RUN pip install -U Daphne
RUN pip install coolsms_python_sdk
RUN pip install python_telegram_bot
RUN pip install websockets
# redis
# pip install pypiwin32

COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install django_extensions

# 옵션 설정
COPY . .
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput


