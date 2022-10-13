from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Currency(models.Model):
    name = models.CharField(max_length=20)
    sign = models.CharField(max_length=1)


class Account(models.Model):
    name = models.CharField(max_length=50)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    calculated = models.BooleanField(default=False)
    datetime = models.DateTimeField(default=now)


class Convertation(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    source_transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='source_in_convertation')
    target_transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='target_in_convertation')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_in = models.DecimalField(max_digits=10, decimal_places=2)


class Cost(models.Model):
    transacton = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    source_transacton = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='source_in_cost')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_in_default_currency = models.DecimalField(max_digits=10, decimal_places=2)
