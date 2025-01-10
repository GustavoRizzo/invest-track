# Create the base image
ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-alpine AS base

# Update the system and install needed packages
RUN apk update && apk upgrade
RUN apk add --update build-base gcc make git bash curl libffi-dev openssl-dev zlib zlib-dev jpeg-dev freetype freetype-dev

# Create the APP Image
FROM base as django
ARG PYTHON_VERSION

RUN mkdir /app
WORKDIR /app

RUN pip install uv

COPY ./pyproject.toml pyproject.toml
COPY ./uv.lock uv.lock
RUN uv sync

COPY ./manage.py ./manage.py
COPY ./ ./

# Static files
RUN uv run python manage.py collectstatic --noinput

## DEV is used in development environment
FROM django as dev

# Run worker and server
CMD uv run python manage.py rqworker & \
    uv run python manage.py runserver 0.0.0.0:8000

## PROD contains the frontend application served by nginx
FROM django AS prod

# Expose a porta 80
EXPOSE 80

# Run worker, server and nginx
CMD uv run python manage.py rqworker & \
    gunicorn -c gunicorn.py "core.wsgi:application" && \
    nginx -g "daemon off;"
