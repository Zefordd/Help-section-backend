# Help section backend

## Setup with docker
Clone the repository:

    $ git clone https://github.com/Zefordd/help_section_backend.git

    $ cd help_section_backend/src
    $ docker-compose build
    $ docker-compose up -d

Fill database with test data:

    $ docker exec -it help_section_backend_container sh entrypoint.sh

Run tests:

    $ docker exec -it help_section_backend_container pytest 


## Setup with virtualenv
Clone the repository:

    $ git clone https://github.com/Zefordd/help_section_backend.git
    $ cd help_section_backend

Make sure Python 3.10+ is installed on your machine

Create virtual env

    $ virtualenv -p python3.10 envname
    # or
    $ python3.10 -m venv

    $ source venv/bin/activate

    $ cd src
    $ pip install -r requirements.txt

Setup database

    # Copy .env file (from src folder)
    $ cp ../env-local-example.env .env
    
    # Create postgres db with creds from .env file or specify your own

    # Fill database with test data:
    $ sh entrypoint.sh
    
    # Run tests:
    $ pytest

Run server

$ python manage.py runserver

## Getting started

Go to http://0.0.0.0:8000/ if you use docker or to http://127.0.0.1:8000/ if you run server with virtualenv

To play with API you can authorize via swagger with these credentials:

    Username: superadmin
    Password: superadmin
