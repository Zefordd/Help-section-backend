#!/bin/sh

export $(cat .env | xargs)

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations
python manage.py migrate

## DEV data creation
python manage.py create_groups
python manage.py dev_create_users
