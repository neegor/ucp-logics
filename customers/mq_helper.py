import logging
import pika
from django.conf import settings

logger = logging.getLogger(__name__)


class RabbitMQPublisher:

    connection = None
    channel = None

    def __init__(self):
        self.connection = self.get_connection()
        self.get_channel()

    def get_connection(self):
        # Создание соединения
        rabbit_settings = settings.RABBITMQ.get('default')

        credentials = pika.PlainCredentials(
            username=rabbit_settings.get('USER'),
            password=rabbit_settings.get('PASSWORD'),
        )
        parameters = pika.ConnectionParameters(
            host=rabbit_settings.get('HOST'),
            port=rabbit_settings.get('PORT'),
            virtual_host=rabbit_settings.get('VIRTUAL_HOST'),
            credentials=credentials
        )
        connection = pika.BlockingConnection(parameters)
        print(f"[RabbitMQ] Connection initialized")
        return connection

    def get_channel(self):
        if self.channel is not None and self.channel.is_open and self.connection.is_open:
            return self.channel

        self.channel = self.get_connection().channel()

        # очереди
        for queue_name in [settings.INDEX_QUEUE_NAME, settings.PERFORM_QUEUE_NAME, ]:
            # self.channel.queue_delete(queue=queue_name)
            resp_declared = self.channel.queue_declare(
                queue=queue_name,
                durable=True,
                # exclusive=False,
                # auto_delete=False,
            )
            print(f"[RabbitMQ] Queue declared: {queue_name}, messages in queue: {resp_declared.method.message_count}")

        return self.channel

    def get_queue_size(self, queue_name):

        if self.channel is None or not self.channel.is_open or not self.connection.is_open:
            self.channel = self.get_connection().channel()

        resp_declared = self.channel.queue_declare(
            queue=queue_name,
            durable=True,
            # exclusive=False,
            # auto_delete=False,
        )
        return resp_declared.method.message_count
