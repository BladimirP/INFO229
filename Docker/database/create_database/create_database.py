import mysql.connector
import os, time

def create_database(db_connection,db_name,cursor):
	cursor.execute(f"CREATE DATABASE {db_name};")
	cursor.execute(f"COMMIT;")
	cursor.execute(f"USE {db_name};")
	
	# Tabla news
	cursor.execute('''CREATE TABLE news (
		id_news INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
		url TEXT,
		title TEXT, 
		date DATE,
		media_outlet VARCHAR(50),
		category VARCHAR(100)
        );''')

	cursor.execute("COMMIT;") 

def insert_data(cursor):
    print("insert")
    cursor.execute('''INSERT INTO news (title,date, url,media_outlet,category) VALUES
	('Conflicto Mapuche', '2021-10-18', 'https://www.elmostrador.cl/claves/conflicto-mapuche/', 'Pagina Web, 'Conflicto'),
    ('Falsedades del Covid19', '2021-05-12','https://iris.paho.org/handle/10665.2/53901','Infodemia', 'Salud'),
	('Asamblea General de la ONU','2021-09-20','https://elpais.com/hemeroteca/2021-09-20/','Pagina Web', 'Politica'),
	('El Oporto tumba al Benfica', '2020-12-31', 'https://as.com/futbol/2021/12/30/internacional/1640841807_994671.html', 'Diario web'),
	('Quinto Retiro AFP', '2021-12-30', 'https://chile.as.com/chile/2021/12/30/actualidad/1640860616_372550.html', 'Diario web'),
	('Resiliencia al Covid', '2021-12-29', 'https://www.df.cl/noticias/economia-y-politica/pais/resiliencia-al-covid-cual-es-la-razon-del-exito-de-chile/2021-12-29/163053.html', 'Diario')
	''')
    cursor.execute("COMMIT;") 

#######################
DATABASE = "tarea2"

DATABASE_IP = str(os.environ['DATABASE_IP'])

DATABASE_USER = "root"
DATABASE_USER_PASSWORD = "root"
DATABASE_PORT=3306

not_connected = True

while(not_connected):
	try:
		print(DATABASE_IP,"IP")
		db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,port=DATABASE_PORT, password=DATABASE_USER_PASSWORD)
		not_connected = False

	except Exception as e:
		time.sleep(3)
		print(e, "error!!!")
		print("can't connect to mysql server, might be intializing")
		
cursor = db_connection.cursor()

try:
	cursor.execute(f"USE {DATABASE}")
	print(f"Database: {DATABASE} already exists")
except Exception as e:
    create_database(db_connection,DATABASE,cursor)
    insert_data(cursor)
    print(f"Succesfully created: {DATABASE}")
