# syntax=docker/dockerfile:1
FROM python:3.8-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
RUN pip3 install --upgrade pip setuptools
COPY requirements.txt /usr/src/app/requirements.txt
#RUN pip install pipenv
RUN cd /usr/src/app && pip install -r requirements.txt
COPY . /usr/src/app
