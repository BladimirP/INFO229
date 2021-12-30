import mysql.connector
import os, time

def create_database(db_connection,db_name,cursor):
	cursor.execute(f"CREATE DATABASE {db_name};")
	cursor.execute(f"COMMIT;")
	cursor.execute(f"USE {db_name};")
	
	# Tabla news
	cursor.execute('''CREATE TABLE pokemon (
		id_pokemon INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
		nombre VARCHAR(20),
		image VARCHAR(200),
		hp INT
		);''')

	cursor.execute("COMMIT;") 

def insert_data(cursor):
    print("insertando Pokemon(s) base")
    cursor.execute('''INSERT INTO pokemon (nombre, image, hp) VALUES
    ('Cyndaquil', 'https://c.tenor.com/Q1GffEXQrgAAAAAi/cyndaquil-pokemon.gif', 39);''')
    
    cursor.execute('''INSERT INTO pokemon (nombre,image,HP) VALUES
    ('Chikorita', 'https://cdn.streamelements.com/uploads/e096efc8-4cb6-4f08-8bdd-6973f0303341.gif', 45);''')
	
    cursor.execute('''INSERT INTO pokemon (nombre,image,HP) VALUES
    ('Totodile', 'https://24.media.tumblr.com/0b8730a22d52a2e82cbde09c447dc00b/tumblr_msu13zuFZ31scncwdo1_500.gif', 50);''')

    cursor.execute('''INSERT INTO pokemon (nombre,image,HP) VALUES
    ('Sentret', 'https://c.tenor.com/mHsYxv4cb4cAAAAi/sentret-sentret-sunday.gif', 35);''')

    cursor.execute('''INSERT INTO pokemon (nombre,image,HP) VALUES
    ('HootHoot', 'https://64.media.tumblr.com/5e591b3f18598d0f4ba7f2bb5050c6ea/badc8ee4f4262685-b5/s500x750/cb76a1fa271de414d5366a0b13b46aff5a6ca50b.gif', 60);''')

    cursor.execute('''INSERT INTO pokemon (nombre,image,HP) VALUES
    ('Spinarak', 'https://pa1.narvii.com/6715/6b5de5585082f3148a7a57aa0385be4750924ac8_hq.gif', 40);''')

    cursor.execute("COMMIT;") 

#######################

def main():
	print("start creating database...")

	DATABASE = "pokedex"

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
