import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

if (len(sys.argv) != 3):
    print('ejecutar como : python3 productor.py wikipedia consulta')
else:
    message = ' '.join(sys.argv[1:])

    #Publicamos los mensajes a través del exchange 'logs' 
    channel.basic_publish(exchange='logs', routing_key='', body=message)

    print(" [x] Sent %r" % message)
connection.close()