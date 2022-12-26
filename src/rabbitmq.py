import json

import pika


class RabbitMq:
    def __init__(self, host, exchange_name, queue_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.exchange_name = exchange_name
        self.channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
        self.channel.queue_declare(queue=queue_name)
        self.channel.queue_bind(exchange=exchange_name, queue=queue_name)

    def publish(self, message):
        self.channel.basic_publish(exchange=self.exchange_name, routing_key='', body=json.dumps(message))
