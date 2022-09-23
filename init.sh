#!/bin/bash
#./manage.py flush --noinput
mv db.sqlite3 db.sqlite3.save
./manage.py makemigrations
./manage.py migrate
rm -rf media/users
./manage.py loaddata settings/initial/users.json 
