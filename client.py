import pika
import os
import sys


def client():
    try:
        host = sys.argv[1]
    except IndexError:
        print('You did not pass arguments. Example: python client.py [server ip address]')
        return
    credentials = pika.PlainCredentials('guest', 'guest')
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host, 5672, '/', credentials))
    except:
        print('Your RabbitMQ not run')
        return
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


if __name__ == '__main__':
    client()

