import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

arguments = {
    'x-queue-type': 'classic'
}

# Создание очередей
channel.queue_declare(queue='file_queue', durable=True, arguments=arguments)
channel.queue_declare(queue='tdf_result', durable=True, arguments=arguments)