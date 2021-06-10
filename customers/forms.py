from django import forms


class AddCustomersForm(forms.Form):
    """Форма для добавления новых пользователей в базу.
    """
    quantity = forms.IntegerField(min_value=1)


class AddQueueTasksForm(forms.Form):
    """Форма для добавления новых задач в очередь.
    """
    quantity = forms.IntegerField(min_value=1)
