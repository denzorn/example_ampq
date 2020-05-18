import pika
import os
import sys

host = sys.argv[1]
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host, 5672, '/', credentials))

channel = connection.channel()
channel.queue_declare(queue='dir_files')

def callback(ch, method, properties, body):
    os.system('clear')
    for root, dirs, files in eval(body):
        level = root.count('/')
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' *4 * (level + 1)
        for file in files:
            print('{}{}'.format(subindent, file))

channel.basic_consume(queue='dir_files', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
