#!/bin/bash
python manage.py makemigrations
python manage.py migrate

## DEV data creation
python manage.py create_groups
python manage.py dev_create_users
