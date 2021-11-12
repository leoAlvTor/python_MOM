import pika
import threading


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


def send_message():
    while True:
        value = str(input('Enter el mensaje: '))
        if value == 'exito':
            break
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=value)
        print('Message sent.')


def main():
    connection2 = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection2.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

thread = threading.Thread(target=send_message)
thread.start()

main()
