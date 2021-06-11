import time

from model_mommy import mommy
from customers.models import Customer


def add_customers(qty=1000):
    """Добавляет новых пользователей в БД.

    Args:
        qty: количество пользователей к добавлению

    Added 1000000 customers in 188.868 seconds. (chunk_size=5000)
    Added 1000000 customers in 190.461 seconds. (chunk_size=1000)
    Added 1000000 customers in 204.128 seconds. (chunk_size=10000)

    Added 1000000 customers in 203.972 seconds. (chunk_size=5000)
    Added 1000000 customers in 203.666 seconds. (chunk_size=5000)
    Added 1000000 customers in 206.289 seconds. (chunk_size=5000)

    15.000 апдейтов
    15.000.000 рассылок

    """

    chunk_size = 5000

    ctr = 0

    chunks_qty = int(qty / chunk_size)
    remains = qty

    start_time = time.time()

    for i in range(chunks_qty):
        if i < (chunks_qty - 1):
            # full chunk

            objects = mommy.prepare(Customer, _quantity=chunk_size, _fill_optional=True)
            remains -= chunk_size
            ctr += chunk_size
        else:
            # the rest
            objects = mommy.prepare(Customer, _quantity=remains, _fill_optional=True)
            ctr += chunk_size

        Customer.objects.bulk_create(objects)
        print(f"Added {ctr} of {qty} customers so far...")

    print(f"Added {qty} customers in {(time.time() - start_time):.3f} seconds. (chunk_size={chunk_size})")


def delete_customers(qty=1000):
    """
    Удаляет N первых пользователей
    """
    start_time = time.time()

    # Получает список id и удаляет записи с этими id
    ids_list = Customer.objects.values_list('pk', flat=True)[:qty]
    deleted_qty, _ = Customer.objects.filter(id__in=ids_list).delete()

    print(f"Deleted {deleted_qty} customers in {(time.time() - start_time):.3f} seconds.")
