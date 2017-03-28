sinvel
===============================

Getting Started
---------------

- Change directory into your newly created project.

    cd sinvel

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    ./env/Scripts/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    ./env/Scripts/pip install -e ".[testing]"

- Configure the database.

    ./env/Scripts/initialize_sinvel_db development.ini

- Run your project's tests.

    ./env/Scripts/pytest

- Run your project.

    ./env/Scripts/pserve development.ini