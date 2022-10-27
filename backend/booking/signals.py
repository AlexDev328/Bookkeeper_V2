from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from booking.models import Transaction
from booking.services.transaction import process_transaction
from booking.tasks import calculate_selfcost_transaction


@receiver(pre_save, sender=Transaction)
def process_transaction_signal(sender, instance, **kwargs):
    process_transaction(instance)

from django.db import transaction
@receiver(post_save, sender=Transaction)
def calc_transaction_signal(sender, instance,  **kwargs):
    print(f'Вызван обработчик для {str(instance)}')
    calculate_selfcost_transaction.delay(instance.id)
    #transaction.on_commit(lambda: calculate_selfcost_transaction(instance.id))
