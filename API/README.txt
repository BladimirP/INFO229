Remplace los terminos from y to por desde y hasta debido a que from
es una palabra reservada. Ademas el nombre de la tablas has_category
es simplemente Category.

ejemplo de la consulta de la tarea:
    http://127.0.0.1:8000/GET/v1/news?desde=0001-01-01&hasta=2022-01-01

Dependencias: 

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