import mysql.connector
import os, time
import pika
import create_database
import random
import pokepy

print("start manager...")
create_database.main()

DATABASE = "pokedex"

DATABASE_IP = str(os.environ['DATABASE_IP'])

DATABASE_USER = "root"
DATABASE_USER_PASSWORD = "root"
DATABASE_PORT=3306

time.sleep(10)
########### CONNEXIÓN A RABBIT MQ #######################

HOST = os.environ['RABBITMQ_HOST']
print("rabbit:"+HOST)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channel = connection.channel()

channel.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

result = channel.queue_declare(queue="cola", exclusive=True, durable=True)
queue_name = result.method.queue

channel.queue_bind(exchange='cartero', queue=queue_name, routing_key="cola")


##############################################################


########## ESPERA Y HACE ALGO CUANDO RECIBE UN MENSAJE #######

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
	print(body.decode("UTF-8"))
	arguments = body.decode("UTF-8").split(" ")

	if(arguments[0]=="!safari"):
		db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,port=DATABASE_PORT, password=DATABASE_USER_PASSWORD)
		cursor = db_connection.cursor()
		cursor.execute(f"USE {DATABASE}")
		cursor.execute(f'''SELECT id_pokemon FROM pokemon ORDER BY id_pokemon DESC LIMIT 1;''')

		for (id_pokemon) in cursor:
			id = random.randint(1, id_pokemon[0])
	
		cursor.execute(f'''SELECT nombre,image,HP FROM pokemon WHERE id_pokemon="{id}";''')

		for (nombre,image, HP) in cursor:
			nombre_pokemon = nombre
			imagen_pokemon = image
			hp_max = HP

		nivel = random.randint(5,15)
		hp_max = (hp_max * nivel) / 10

		result = ("¡Ha aparecido un *{nom}* salvaje!*{ima}*{hp}".format(nom= nombre_pokemon, ima = imagen_pokemon, hp=hp_max))
		print(result)

		########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
		print("send a new message to rabbitmq: "+result)
		channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=result)
	# Lo deje porque cada vez que lo borraba todo el codigo fallaba T.T
	if (arguments[0]=="!birthday"):

		person = arguments[1]
		print(person)
		db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,port=DATABASE_PORT, password=DATABASE_USER_PASSWORD)
		cursor = db_connection.cursor()
		cursor.execute(f"USE {DATABASE}")
		cursor.execute(f'''SELECT member,date FROM birthday WHERE member="{person}";''')
		for (member, date) in cursor:
			result="{} nació el {:%d %b %Y}".format(member,date)
			print(result)

			########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
			print("send a new message to rabbitmq: "+result)
			channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=result)

	if (arguments[0]=="!add-pokemon"):
		
		#coneccion con API de pokemones
		name = arguments[1]
		pokemon = pokepy.V2Client().get_pokemon(name)
		hp_base = pokemon[0].stats[0].base_stat
		imagen = pokemon[0].sprites.front_default

		db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,port=DATABASE_PORT, password=DATABASE_USER_PASSWORD)
		cursor = db_connection.cursor()
		cursor.execute(f"USE {DATABASE}")
		cursor.execute(f'''INSERT INTO pokemon(nombre,image,HP) VALUES("{pokemon[0].name}","{imagen}","{hp_base}");''')
		cursor.execute(f'''COMMIT;''')

		result = ("¡Se ha agregado a *{nom}* a la zona safari!*{ima}*{hp}".format(nom= name, ima = imagen, hp = hp_base))
		print(result)

		########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
		print("send a new message to rabbitmq: "+result)
		channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=result)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()



#######################