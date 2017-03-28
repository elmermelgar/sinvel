sinvel
===============================

Getting Started
---------------

- Ingresa al directorio del proyecto.

    cd sinvel

- Crear un entorno virtual de Python.

    python3 -m venv env

- Actualiza los paquetes de las utilidades.

    ./env/Scripts/pip install --upgrade pip setuptools

- Instala el proyecto in editable mode with its testing requirements.

    ./env/Scripts/pip install -e ".[testing]"

- Copia en el directorio base el archivo ejemplo de desarrollo "example.development.ini" y renombralo a "development.ini"

    copy example.development.ini => development.ini

- Escribe dentro de "development.ini" la cadena de conexión de la base de datos.

    sqlalchemy.url = mysql://usuario:contraseña@localhost:3306/base_de_datos

- Configure la base de datos.

    ./env/Scripts/initialize_sinvel_db development.ini

- Ejecutar la prueba del proyecto.

    ./env/Scripts/pytest

- Correr el proyecto.

    ./env/Scripts/pserve development.ini