import pika
import os
import time
import sys


def server():
    try:
        directory = sys.argv[1]
    except IndexError:
        print('You did not pass arguments. Example: python server.py [path you directory]')
        return
    credentials = pika.PlainCredentials('guest', 'guest')
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
    except:
        print('You RabbitMQ not run')
        return
    channel = connection.channel()
    channel.queue_declare(queue='dir_files')

    list_directory = ''

    while True:
        if list_directory != list(os.walk(directory)):
            list_directory = list(os.walk(directory))
            channel.basic_publish(exchange='', routing_key='dir_files', body=str(list(list_directory)))
        time.sleep(5)
    return


if __name__ == '__main__':
    server()
 
