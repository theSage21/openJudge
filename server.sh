#! /bin/bash
source env/bin/activate
cd openjudge &&
python manage.py collectstatic --noinput &&
gunicorn website.wsgi:application --bind=127.0.0.1:8000 --log-file=- --workers $(nproc)  --threads 3
