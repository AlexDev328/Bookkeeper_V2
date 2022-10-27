from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from datetime import datetime
from django.db.models import signals
from django.utils.timezone import now

from booking.models import Currency, Account, Transaction, Cost, Convertation
from booking.tasks import calculate_selfcost_transaction
from user_profile.models import Profile


class CostTestCase(TestCase):
    def setUp(self):
        signals.post_save.disconnect(sender=Transaction)
        self.ruble = Currency.objects.create(name="RUB", sign="R")
        self.dollar = Currency.objects.create(name="USD", sign="$")
        self.user: User = User.objects.create_user(username="testuser", email='test@user.com', password='123456')
        self.user.profile.default_currency = self.ruble
        self.user.profile.save()
        self.ruble_account = Account.objects.create(name="ruble account", currency=self.ruble, owner=self.user, balance=0)
        self.dollar_account = Account.objects.create(name="dollar account", currency=self.dollar, owner=self.user,
                                                    balance=0)

        

    def test_transaction_in_default_currency(self):
        transaction = Transaction.objects.create(account=self.ruble_account, amount=-10)
        calculate_selfcost_transaction(transaction.id)
        cost = Cost.objects.filter(transaction=transaction).first()
        self.assertIsNotNone(cost)
        self.assertEqual(-10, cost.amount)
        self.assertEqual(-10, cost.amount_in_default_currency)

    def test_currency_exchange_single(self):
        exchange: Convertation = Convertation.objects.create(from_account=self.ruble_account,
                                                             to_account=self.dollar_account,
                                                             amount=1, amount_in=60, datetime=now())
        #TODO: написать отдельный тест, проверяющий порядок пересчета для таких случаев (какая транзакция пересчитывается первой)
        calculate_selfcost_transaction(exchange.source_transaction.id)
        calculate_selfcost_transaction(exchange.target_transaction.id)

        self.assertEqual(1, exchange.source_transaction.cost_set.count())
        source_cost = exchange.source_transaction.cost_set.first()
        self.assertEqual(Decimal(-60), source_cost.amount_in_default_currency)
        self.assertEqual(Decimal(-60), source_cost.amount)

        self.assertEqual(1, exchange.target_transaction.cost_set.count())
        target_cost = exchange.target_transaction.cost_set.first()
        self.assertEqual(Decimal(60), target_cost.amount_in_default_currency)
        self.assertEqual(Decimal(1), target_cost.amount)


    def test_spending_after_currency_exchange(self):
        exchange: Convertation = Convertation.objects.create(from_account=self.ruble_account,
                                                             to_account=self.dollar_account,
                                                             amount=1, amount_in=60, datetime=now())
        calculate_selfcost_transaction(exchange.source_transaction.id)
        calculate_selfcost_transaction(exchange.target_transaction.id)

        transaction = Transaction.objects.create(account=self.dollar_account, amount=-0.5)
        print(f'создали транзакцию с id {transaction.id}')
        calculate_selfcost_transaction(transaction.id)

        self.assertTrue(Cost.objects.filter(transaction=transaction).exists())
        self.assertTrue(transaction.cost_set.exists())
