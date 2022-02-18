# Help section backend

## Setup
Clone the repository:

    $ git clone FIXME

    $ cd help_section_backend/src
    $ docker-compose build
    $ docker-compose up -d

Fill database with test data:

    $ docker exec -it help_section_backend_container sh entrypoint.sh

Run tests:

    $ docker exec -it help_section_backend_container pytest 


Go to http://0.0.0.0:8000/
