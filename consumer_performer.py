import django
import json
import pika

from django.conf import settings

from customers.helpers import add_customers, delete_customers
from customers.models import Customer

django.setup()


def start_performer_consumer():
    """Запускает консьюмер очереди обработчика.
    """

    rabbit_settings = settings.RABBITMQ.get('default')

    credentials = pika.PlainCredentials(
        username=rabbit_settings.get('USER'),
        password=rabbit_settings.get('PASSWORD'),
    )
    parameters = pika.ConnectionParameters(
        host=rabbit_settings.get('HOST'),
        port=rabbit_settings.get('PORT'),
        virtual_host=rabbit_settings.get('VIRTUAL_HOST'),
        credentials=credentials,
    )
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(
        queue=settings.PERFORM_QUEUE_NAME,
        durable=True,
    )

    channel.basic_consume(
        queue=settings.PERFORM_QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=True,
    )

    channel.start_consuming()


def callback(ch, method, properties, body):
    """
    Обрабатывает сообщение из очереди.

    Args:
        ch: канал
        method: метод
        properties: свойства
        body: сообщение из очереди
    """
    print(f" [x] Task received with data: {body}")

    # Декодирование данных
    try:
        data_dict = json.loads(body.decode())

        operation = data_dict.get('type')
        customer_id = data_dict.get('id')

        if operation == "perform":
            try:
                customer = Customer.objects.get(pk=customer_id)
                print(
                    f'Performing customer: first_name={customer.first_name} last_name={customer.last_name} '
                    f'email={customer.email} phone={customer.phone}'
                )
            except Customer.DoesNotExist:
                print(f"Customer with id {customer_id} not found")

    except (TypeError, ValueError, json.JSONDecodeError):
        print(f"Incorrect data received - task skipped")


if __name__ == "main":
    start_performer_consumer()
