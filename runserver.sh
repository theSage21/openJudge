#! /bin/bash
source env/bin/activate

cd openJudge/webserver
gunicorn website.wsgi:application --bind=unix:/home/ghost/dev/gunicorn_socket --log-file=-
