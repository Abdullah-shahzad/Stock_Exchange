from dataclasses import fields
from rest_framework import serializers
from stock_exchange_app.models import User, Stocks, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'balance']

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = ['ticker', 'stock_price', 'stock_name']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user', 'ticker', 'transaction_type', 'transaction_volume', 'created_time']




