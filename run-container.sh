#!/bin/sh

# Runs in the docker container, applies migrations and starts the server

/webapp/manage.py migrate

/webapp/manage.py runserver 0.0.0.0:8000