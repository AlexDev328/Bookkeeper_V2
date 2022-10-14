from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from booking.models import Currency, Account, Convertation, Transaction
from booking.serializers import CurrencySerializer, AccountSerializer, TransactionSerializer, ConvertationSerializer
from rest_framework import generics


class CurrencyList(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CurrencyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        # TODO clear
        serializer.save(owner=User.objects.first())


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class ConvertationList(generics.ListCreateAPIView):
    queryset = Convertation.objects.all()
    serializer_class = ConvertationSerializer


class ConvertationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Convertation.objects.all()
    serializer_class = ConvertationSerializer


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
