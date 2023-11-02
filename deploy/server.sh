#!/bin/bash

DJANGODIR=$(dirname $(cd `dirname $0` && pwd))
DJANGO_SETTINGS_MODULE=mysite.settings
cd $DJANGODIR
source env/bin/activate

export DJANGO_SETTING_MODULE=$DJANGO_SETTINGS_MODULE
exec python manage.py runserver 0:8000
