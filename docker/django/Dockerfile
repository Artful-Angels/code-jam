# pull the official base image
FROM python:3.9-slim

# set work directory
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip
COPY ./backend/requirements.txt backend/requirements.txt
WORKDIR /app/backend
RUN pip install -r requirements.txt

# copy project
COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
