from django.contrib.auth.models import User
from django.db.models import signals
from django.test import TestCase


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
        self.ruble_account = Account.objects.create(name="ruble account", currency=self.ruble, owner=self.user,
                                                    balance=0)
        self.dollar_account = Account.objects.create(name="dollar account", currency=self.dollar, owner=self.user,
                                                     balance=0)



    def test_create_without_transactions(self):
        exchange: Convertation = Convertation.objects.create(from_account=self.ruble_account,
                                                             to_account=self.dollar_account,
                                                             amount=1, amount_in=60, datetime=now())
        self.assertIsNotNone(exchange.target_transaction)
        self.assertIsNotNone(exchange.source_transaction)
        self.assertEqual(-60, exchange.source_transaction.amount)
        self.assertEqual(1, exchange.target_transaction.amount)

    def test_create_with_source_transaction(self):
        ruble_transaction = Transaction.objects.create(account=self.ruble_account, amount=-60)
        exchange: Convertation = Convertation.objects.create(from_account=self.ruble_account,
                                                             to_account=self.dollar_account,
                                                             source_transaction=ruble_transaction,
                                                             amount=1, amount_in=-ruble_transaction.amount,
                                                             datetime=now())
        self.assertEqual(ruble_transaction, exchange.source_transaction)
        self.assertIsNotNone(exchange.target_transaction)
        self.assertEqual(1, exchange.target_transaction.amount)

    def test_create_with_target_transaction(self):
        dollar_transaction = Transaction.objects.create(account=self.dollar_account, amount=1)
        exchange: Convertation = Convertation.objects.create(from_account=self.ruble_account,
                                                             to_account=self.dollar_account,
                                                             amount=dollar_transaction.amount, amount_in=60,
                                                             datetime=now(),
                                                             target_transaction=dollar_transaction)
        self.assertIsNotNone(exchange.source_transaction)
        self.assertEqual(-60, exchange.source_transaction.amount)
        self.assertEqual(dollar_transaction, exchange.target_transaction)
