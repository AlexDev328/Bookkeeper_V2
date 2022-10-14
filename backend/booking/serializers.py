from rest_framework import serializers
from booking.models import Currency, Transaction, Convertation, Account


class CurrencySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=20)
    sign = serializers.CharField(required=True, max_length=1)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Currency.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('name', instance.name)
        instance.code = validated_data.get('sign', instance.sign)
        instance.save()
        return instance


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'currency', 'balance']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'amount', 'datetime']


class ConvertationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Convertation
        fields = ['id', 'from_account', 'to_account', 'source_transaction_id', 'target_transaction_id', 'amount', 'amount_in']
