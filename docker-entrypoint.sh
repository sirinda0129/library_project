#!/bin/sh

cd /opt/app
python manage.py migrate
uwsgi --ini uwsgi.ini --die-on-term