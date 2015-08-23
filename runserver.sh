#! /bin/bash
source env/bin/activate

cd openJudge/webserver
# gunicorn website.wsgi:application --bind=127.0.0.1:8000 --log-file=-
gunicorn website.wsgi:application --bind=unix:/home/ghost/dev/openJudge/openJudge/gunicorn_socket --log-file=-
