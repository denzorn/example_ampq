import pika
import os
import time
import sys

directory = sys.argv[1]
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='dir_files')

list_directory = ''

while True:
    if list_directory != list(os.walk(directory)):
        list_directory = list(os.walk(directory))
        channel.basic_publish(exchange='', routing_key='dir_files', body=str(list(list_directory)))
    time.sleep(5)
 
