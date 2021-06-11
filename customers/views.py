import json
import time

from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from model_mommy import mommy

from customers.forms import AddCustomersForm, AddQueueTasksForm
from customers.models import Customer
from customers.mq_helper import RabbitMQPublisher


mq_publisher = RabbitMQPublisher()


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
            # Вызов таска на добавление пользователей
            mq_publisher.get_channel().basic_publish(
                exchange='',
                routing_key=settings.INDEX_QUEUE_NAME,
                body=json.dumps(
                    {
                        'type': 'add',
                        'qty': quantity,
                    }
                )
            )

            messages.add_message(
                self.request,
                messages.SUCCESS,
                f"Будет создано {quantity} новых пользователей."
            )
        elif '_delete' in self.request.POST:
            # Вызов таска на удаление пользователей
            mq_publisher.get_channel().basic_publish(
                exchange='',
                routing_key=settings.INDEX_QUEUE_NAME,
                body=json.dumps(
                    {
                        'type': 'delete',
                        'qty': quantity,
                    }
                )
            )

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

        # Получает число тасков в очереди/топике
        kwargs['queue_tasks_count'] = mq_publisher.get_queue_size(settings.PERFORM_QUEUE_NAME)
        return kwargs

    def form_valid(self, form):
        """Вызывается, когда была отправлена корректная форма.

        Returns:
            Объект ответа HttpResponse
        """
        quantity = form.cleaned_data['quantity']

        if '_add' in self.request.POST:

            # Вызов таска на добавление тасков в очередь обработки
            for customer_id in Customer.objects.order_by('?').values_list('pk', flat=True)[:quantity]:
                mq_publisher.get_channel().basic_publish(
                    exchange='',
                    routing_key=settings.PERFORM_QUEUE_NAME,
                    body=json.dumps(
                        {
                            'type': 'perform',
                            'id': customer_id,
                        }
                    )
                )

            messages.add_message(
                self.request,
                messages.SUCCESS,
                f"{quantity} новых задач было добавлено в очередь."
            )
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                f"Некорректный запрос."
            )
        return super().form_valid(form)
