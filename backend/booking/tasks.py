from celery import shared_task
from django.db.models import Sum, Q, DecimalField
from django.db.models.functions import Coalesce

from booking.models import Transaction, Cost


@shared_task
def calculate_selfcost_transaction(transaction_id: int):
    print(f'расчитываю себестоимость транзакции №{transaction_id}')
    transaction: Transaction = Transaction.objects.get(id=transaction_id)
    print(transaction)
    # Если транзакция уже обсчитана
    if transaction.calculated:
        print("транзакиця уже обсчитана")
        return
    # Если транзакция в дефолтной валюте
    print(f"default currency {transaction.account.owner.profile.default_currency_id}")
    print(f"transaction currency {transaction.account.currency.id}")
    if transaction.account.owner.profile.default_currency_id == transaction.account.currency.id:
        Cost.objects.create(
            transaction=transaction,
            amount=transaction.amount,
            amount_in_default_currency=transaction.amount
        )
        transaction.calculated = True
        transaction.save()
        return

    print(f"transaction.target_in_convertation.first() {transaction.target_in_convertation.first()}")

    if transaction.target_in_convertation.first() is not None:
        sr_transaction = transaction.target_in_convertation.first().source_transaction
        if sr_transaction.calculated:
            amount_in_def_currency = \
                sr_transaction.cost_set.aggregate(amount_in_def_cur=Sum('amount_in_default_currency'))[
                    'amount_in_def_cur']

            Cost.objects.create(
                transaction=transaction,
                amount=transaction.amount,
                source_transaction_id=sr_transaction.id,
                amount_in_default_currency=-amount_in_def_currency
            )
            transaction.calculated = True
            transaction.save()
            return

    # получаем количество свободной вылюты
    # конвертации со свободной валютой
    # поиск свободной валюты
    transactions = Transaction.objects.filter(Q(amount__gt=0) & Q(account__currency=transaction.account.currency)) \
        .annotate(free_amount=Sum('amount') + Coalesce(Sum('source_in_cost'), 0,
                                                       output_field=DecimalField()))

    print(transactions.query)
    print(transactions)
    print(transactions[0])

    if transactions.aggregate(max_amount=Sum('free_amount'))['max_amount'] < transaction.amount:
        return
    needed_amount = transaction.amount

    for i in transactions:
        tr_amount_in_def_cut = i.cost_set.aggregate(amount_in_def_cur=Sum('amount_in_default_currency'))[
            'amount_in_def_cur']
        if tr_amount_in_def_cut is None:
            continue
        if i.free_amount < needed_amount:
            Cost.objects.create(transaction=transaction, source_transaction=i, amount=i.free_amount,
                                amount_in_default_currency=tr_amount_in_def_cut)
            needed_amount -= i.free_amount
        else:
            needed_amount_in_def_cur = tr_amount_in_def_cut / i.amount * needed_amount

            Cost.objects.create(transaction=transaction, source_transaction=i, amount=needed_amount,
                                amount_in_default_currency=needed_amount_in_def_cur)
            transaction.calculated = True
            transaction.save()

