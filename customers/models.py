from django.contrib.postgres.indexes import BrinIndex
from django.db import models


class Customer(models.Model):
    """Модель клиента.
    """
    first_name = models.CharField(max_length=32, null=False, blank=False, verbose_name="Имя")
    last_name = models.CharField(max_length=32, null=False, blank=False, verbose_name="Фамилия")
    email = models.EmailField(max_length=64, null=True, blank=True, verbose_name="E-mail")
    phone = models.CharField(max_length=32, null=True, blank=True, verbose_name="Телефон")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

        indexes = [
            # BrinIndex(fields=['first_name', 'last_name',])
            BrinIndex(fields=['first_name'], pages_per_range=32),
            # BrinIndex(fields=['last_name'], pages_per_range=32),
            # BrinIndex(fields=['email'], pages_per_range=32),
            # BrinIndex(fields=['phone'], pages_per_range=32),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}, email: {self.email} tel.: {self.phone}"
