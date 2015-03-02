#! /bin/bash
SOCKFILE=/home/ghost/dev/programming/gunicorn.sock
gunicorn -b unix:$SOCKFILE --log-file=- website.wsgi:application
