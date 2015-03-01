#! /bin/bash
gunicorn -b 127.0.0.1:8000 --log-file=- website.wsgi:application
