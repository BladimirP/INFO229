sudo apt update

sudo apt install python3-pip

pip install uvicorn

pip install fastapi

pip install sqlalchemy

pip install mysql-connector-python

sudo apt install mariadb-server

CREATE USER 'my-api'@'localhost' IDENTIFIED BY 'my-api-password';
GRANT ALL PRIVILEGES ON * . * TO 'my-api'@'localhost';

CREATE DATABASE tarea1;