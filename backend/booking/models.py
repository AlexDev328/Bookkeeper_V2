from decimal import Decimal

from django.db.transaction import atomic
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
    source_transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='source_in_convertation',
                                           blank=True)
    target_transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='target_in_convertation',
                                           blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_in = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField(default=now, blank=True)

    @atomic
    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.source_transaction_id is None:
            self.source_transaction = Transaction(account=self.from_account, amount=-self.amount_in)

        if self.target_transaction_id is None:
            self.target_transaction = Transaction(account=self.to_account, amount=self.amount)

        super(Convertation, self).save(force_insert, force_update, using, update_fields)



class Cost(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    source_transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='source_in_cost', null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_in_default_currency = models.DecimalField(max_digits=10, decimal_places=2)
