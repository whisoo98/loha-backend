# pull official base image
FROM python:3.8.6-alpine

RUN apk update && apk add bash
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install git into container
#RUN apt-get install git -y

# install dependencies
RUN pip install --upgrade pip
RUN pip install requests
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
