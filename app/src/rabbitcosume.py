import json
import base64
import socket

import docker
import pika
from preprocessing import Pipeline

pipeline = Pipeline()

client = docker.from_env()
network_name = "mynetwork"
atp_container = client.containers.get(socket.gethostname())
client.networks.get(network_name).connect(container=atp_container.id)

connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@rabbitmq/"))
channel = connection.channel()
def publishTagsAndId(user_id, tags: dict):
    message = json.dumps(tags)

    properties = pika.BasicProperties(
        headers={'id': user_id}
    )

    channel.basic_publish(
        exchange='',
        routing_key='tdf_result',
        body=message,
        properties=properties
    )
    print(" [x] Sent tags for user {}.".format(user_id))


def callback(ch, method, properties, body):
    file_id = properties.headers.get('id')

    if file_id is not None:
        print(f"Received file with id {file_id} ")
    else:
        print("Received file with missing or incomplete header information")
        return

    text = base64.b64decode(body).decode('utf-8')
    pipeline.set_text(text)
    pipeline.process()
    processed_tags = pipeline.get_tags()
    publishTagsAndId(file_id, processed_tags)

channel.basic_consume(queue='file_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()