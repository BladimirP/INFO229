import pika
import pageviewapi.period

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    message = body.decode("UTF-8")
    message = message.split(' ')
    visitas = pageviewapi.period.sum_last('en.wikipedia', message[1] , last=30,
                            access='all-access', agent='all-agents')
    
    print(" [x] En los ultimos 30 dias han habido {num} visitas en {consulta}".format(num=visitas, consulta = message[1]))

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

