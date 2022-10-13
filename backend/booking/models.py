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
