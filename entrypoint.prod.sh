#!/bin/sh

python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput
python3 -m gunicorn --bind 0.0.0.0:8000 --workers 3 capstone.wsgi:application