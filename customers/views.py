import time

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from model_mommy import mommy

from customers.forms import AddCustomersForm, AddQueueTasksForm
from customers.models import Customer


class IndexView(FormView):
    """Вьюха работы с индексом.

    Позволяет добавлять и удалять новых пользователей.
    """

    template_name = "index.html"
    form_class = AddCustomersForm
    success_url = reverse_lazy('index_view')

    def get_context_data(self, **kwargs):

        kwargs['customers_count'] = Customer.objects.count()

        return kwargs

    def form_valid(self, form):
        """Вызывается, когда была отправлена корректная форма.

        Returns:
            Объект ответа HttpResponse
        """
        quantity = form.cleaned_data['quantity']

        if '_add' in self.request.POST:
            # TODO: вызов таска на добавление пользователей

            messages.add_message(
                self.request,
                messages.SUCCESS,
                f"Будет создано {quantity} новых пользователей."
            )
        elif '_delete' in self.request.POST:
            # TODO: вызов таска на удаление пользователей

            messages.add_message(
                self.request,
                messages.SUCCESS,
                f"Будет удалено {quantity} пользователей."
            )
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                f"Некорректный запрос."
            )
        return super().form_valid(form)


class QueueView(FormView):
    """Вьюха работы с очередью.

    Позволяет добавлять задачи на обработку в очередь.
    """

    template_name = "queue.html"
    form_class = AddQueueTasksForm
    success_url = reverse_lazy('queue_view')

    def get_context_data(self, **kwargs):

        # TODO: Получить число тасков в очереди/топике
        # kwargs['queue_tasks_count'] =
        return kwargs

    def form_valid(self, form):
        """Вызывается, когда была отправлена корректная форма.

        Returns:
            Объект ответа HttpResponse
        """
        quantity = form.cleaned_data['quantity']

        if '_add' in self.request.POST:
            # TODO: вызов таска на добавление тасков в очередь

            messages.add_message(
                self.request,
                messages.SUCCESS,
                f"Будет создано {quantity} новых задач."
            )
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                f"Некорректный запрос."
            )
        return super().form_valid(form)


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

    chunks_qty = int(qty/chunk_size)
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


def clean_customers():
    """

    Returns:
    """
    print(Customer.objects.all().delete())
