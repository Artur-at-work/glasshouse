# syntax=docker/dockerfile:1
FROM python:3.8-bullseye
#FROM python:3.9.5-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
#RUN pip install pipenv
RUN cd /usr/src/app && pip install -r requirements.txt
COPY . /usr/src/app
