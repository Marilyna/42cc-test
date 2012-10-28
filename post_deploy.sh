#!/bin/sh

rev_path=`pwd`
config_path=`dirname ${rev_path}`/uwsgi

if [ ! -f ../deploy.sqlite3 ]
then
    PYTHONPATH="${config_path}:${rev_path}" django-admin.py syncdb --noinput --settings settings_deploy
fi

PYTHONPATH="${config_path}:${rev_path}" django-admin.py collectstatic --noinput --settings settings_deploy