#! /bin/bash
gunicorn website.wsgi:application --bind=unix:/home/ghost/dev/gunicorn.socket --log-file=-
