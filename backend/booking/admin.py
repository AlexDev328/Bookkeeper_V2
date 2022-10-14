from django.contrib import admin

# Register your models here.
from booking.models import Currency, Account, Transaction, Convertation


admin.site.register(Currency)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Convertation)